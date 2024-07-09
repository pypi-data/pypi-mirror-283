import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
from math import sqrt
from collections import OrderedDict

import os
import re
import csv
import yaml
import pickle
import random
from .model import LSTMModel
import matplotlib.pyplot as plt
import requests

class Test_model:
    def create_inout_sequences(self,input_data,input_label, tw):
        inout_seq = []
        L = len(input_data)
        for i in range(L-tw):
            train_seq = input_data[i:i+tw]
            train_label = input_label[i+tw]
            inout_seq.append((train_seq, train_label))
        return inout_seq

    def deal_with_mape(self,actuals, pretrained_prediction, finetuned_prediction):
        actuals_array = np.array(actuals)
        zero_pos = np.where(actuals_array==0)
        non_zero_actuals_array = np.delete(actuals_array, zero_pos)

        predictions_array = np.array(pretrained_prediction)
        non_zero_pretrained_predictions_array = np.delete(predictions_array, zero_pos)

        predictions_array = np.array(finetuned_prediction)
        non_zero_finetuned_predictions_array = np.delete(predictions_array, zero_pos)
        return non_zero_actuals_array.tolist(), non_zero_pretrained_predictions_array.tolist(), non_zero_finetuned_predictions_array.tolist()

    def data_to_csv(self,actual_data, global_data, model_type, path, filename, bs_id):
        with open(os.path.join(path, f'bs{bs_id}_actual_{filename}'), 'w', newline='') as file:
            writer = csv.writer(file)
        
            headers = ['Timestep']
            for ue in actual_data['ue_data']:
                headers.extend([f'{ue}_actuals'])
            writer.writerow(headers)

            combined_data = [actual_data['timestep']]
            for ue in actual_data['ue_data'].values():
                actuals = ue
                combined_data.append(actuals)

            for row in zip(*combined_data):
                writer.writerow(row)

        self.upload_metrics(file_path=os.path.join(path, f'bs{bs_id}_actual_{filename}'))

        with open(os.path.join(path, f'bs{bs_id}_{model_type}_{filename}'), 'w', newline='') as file:
            writer = csv.writer(file)
        
            headers = ['Timestep']
            for ue in global_data['ue_data']:
                headers.extend([f'{ue}_actuals', f'{ue}_predictions'])
            writer.writerow(headers)

            combined_data = [global_data['timestep']]
            for ue in global_data['ue_data'].values():
                actuals, predictions = ue
                combined_data.append(actuals)
                combined_data.append(predictions)

            for row in zip(*combined_data):
                writer.writerow(row)

        self.upload_metrics(file_path=os.path.join(path, f'bs{bs_id}_{model_type}_{filename}'))
    def resource_utilization(self,ground_truths, predictions):
        resource_usages = []
        for gt, pred in zip(ground_truths, predictions):
            if pred<=0:
                resource_usages.append(1)
            else:
                resource_usages.append(min(gt / pred, 1)) 

        average_resource_usage = sum(resource_usages) / len(resource_usages)

        return average_resource_usage
        
    def under_and_over_estimations(self,ground_truths, predictions):
        # calculate diff
        differences = [prediction - truth for prediction, truth in zip(predictions, ground_truths)]

        # split to under and over estimation
        under_estimations = [diff for diff in differences if diff < 0]
        over_estimations = [diff for diff in differences if diff > 0]  
        # average
        avg_under_estimation = sum(under_estimations) / len(under_estimations) if under_estimations else 0
        avg_over_estimation = sum(over_estimations) / len(over_estimations) if over_estimations else 0

        mae = mean_absolute_error(ground_truths, predictions)
        return mae, abs(avg_under_estimation), avg_over_estimation 

    def sum_of_usage(self,ground_truths, predictions):

        return sum(ground_truths), sum(predictions)

    def calculate_metrics(self,actuals, predictions):
        metrics = {}
        metrics['rmse'] = sqrt(mean_squared_error(actuals, predictions))
        metrics['r2_score'] = r2_score(actuals, predictions)
        metrics['mae'], metrics['under_estimation'], metrics['over_estimation'] = self.under_and_over_estimations(actuals, predictions)
        metrics['resources_utilization'] = self.resource_utilization(actuals, predictions)
        metrics['ground_truth_usage'], metrics['prediction_usage'] = self.sum_of_usage(actuals, predictions)

        return metrics

    def set_plt_title(self,name, show_metrics, front_pretrained_metrics, back_pretrained_metrics, finetuned_metrics, ax):
        if show_metrics == "rmse":
            ax.set_title(f'''
            {name}
            Pre-trained RMSE:{front_pretrained_metrics["rmse"]:.4f} | {back_pretrained_metrics["rmse"]:.4f}
            Fine-tuned RMSE:{finetuned_metrics["rmse"]:.4f}''')

        elif show_metrics == "r2-score":
            ax.set_title(f'''
            {name} 
            Pre-trained R2:{front_pretrained_metrics["r2_score"]:.4f} | {back_pretrained_metrics["r2_score"]:.4f}
            Fine-tuned R2:{finetuned_metrics["r2_score"]:.4f}''')

        elif show_metrics == "mae":
            ax.set_title(f'''
            {name}
            Pre-trained MAE:{front_pretrained_metrics["mae"]:.4f} | {back_pretrained_metrics["mae"]:.4f}
            Fine-tuned MAE:{finetuned_metrics["mae"]:.4f}''')
                
        elif show_metrics == "resources_utilization":
            ax.set_title(f'''
            {name}
            Pre-trained resources utilization:{front_pretrained_metrics["resources_utilization"]*100:.2f}% | {back_pretrained_metrics["resources_utilization"]*100:.2f}%
            Fine-tuned resources utilization:{finetuned_metrics["resources_utilization"]*100:.2f}%''')

        elif show_metrics == "total_usage":
            ax.set_title(f'''
            {name}
            Ground truth total downlink usage:  {front_pretrained_metrics["ground_truth_usage"]:.2f}  | {back_pretrained_metrics["prediction_usage"]:.2f} 
            Pre-trained predict total downlink: {front_pretrained_metrics["prediction_usage"]:.2f} | {back_pretrained_metrics["prediction_usage"]:.2f} 
            Fine-tuned predict total downlink:{finetuned_metrics["prediction_usage"]:.2f}''')

    def metrics_to_json(self,metrics, path, filename, bs_id):
        with open(os.path.join(path, f'bs{bs_id}_{filename}'), 'wb') as pickle_file:
            pickle.dump(metrics, pickle_file)

    def mix_sequences(self,sequence_list):
        bs1_sequnece = sequence_list[0]
        result_sequence = bs1_sequnece[:int(len(bs1_sequnece)*0.67)].copy() #bs1 sequence
        
        test_sequence = []
        for sequence in sequence_list[1:]:
            test_sequence += sequence[:int(len(sequence)*0.33)]

        result_sequence+=test_sequence
        return result_sequence

    def load_yaml(self,file):
        data = yaml.safe_load(file)
        return data

    def upload_metrics(self,file_path):
        url = 'http://140.113.86.26:30808/upload_metrics'
        with open(file_path, 'r', newline='') as f:
            files = {'file': f}
            data = {'string_data': file_path}
            response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            print('Success')
        else:
            print('Fail:', response.status_code, response.text)
        
    def test_mix(self,X_scaler_path, y_scaler_path,  model_path, config):
        random.seed(41)  
        bs_list = [1,2,3,4]
        show_mode = "all"
        # type
        model_type = config['type']
        # network slice
        slice_id = config['slice_id']
        ue_nums = 4 if slice_id !=0 else 3 
        # show_metrics = ["mae", "rmse", "total_usage", "resources_utilization", "r2-score"]
        show_metrics = ["rmse"]
        # exp and result path
        exp_path = config['exp_path']
        result_folder_path = config['result_path']
        # model config
        model_config = config['model'] 
        hidden_size = model_config['hidden_size']
        num_layers = model_config['num_layers']
        # hyperparameters
        hyperparams = config['hyperparameters']
        window_size = hyperparams['window_size']
        fedprox_mu = hyperparams['fedprox_mu']
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {device}")
        # 選擇特徵和標籤
        features = [ 'dl_mcs', 'dl_n_samples', 'dl_buffer [bytes]' ,
                    'tx_pkts downlink', 'dl_cqi',
                    'ul_mcs', 'ul_n_samples', 'ul_buffer [bytes]', 'phr',
                    'rx_brate uplink [Mbps]', 'rx_pkts uplink', 'rx_errors uplink (%)',
                    'ul_sinr', 'sum_requested_prbs',
                    'sum_granted_prbs', 'ul_turbo_iters', 'tx_brate downlink [Mbps]']
        #  or 
        label =  ['tx_brate downlink [Mbps]']
        scaler = joblib.load(X_scaler_path)
        scaler_label = joblib.load(y_scaler_path)

        sequences_list = []
        for i, bs_id in enumerate(bs_list):
            dfs_dict = {}
            UE_path = []
            bs_path = os.path.join(exp_path, f"bs{bs_id}/slices_bs{bs_id}")
            # 加載CSV數據
            bs_files = os.listdir(bs_path)
            df = pd.DataFrame({})
            csv_files = [file for file in bs_files if file.endswith('.csv')]
            # sort the csv_files list
            csv_files.sort()
            csv_file_paths = [os.path.join(bs_path, file) for file in csv_files]
            for csv_file in csv_file_paths:
                df = pd.read_csv(csv_file)
                if df['slice_id'].unique() == slice_id:
                    UE_path.append(csv_file)
                    IMSI = df['IMSI'].unique()[0]
                    df = df[['Timestamp']+features]
                    # add suffix to cols
                    suffix = f"_{IMSI}"
                    df.columns = [f'{col}{suffix}' if col != "Timestamp" else col for col in df.columns]
                    dfs_dict[IMSI] = df
                    
            df_keys = [IMSI for IMSI, _ in dfs_dict.items()]
            # merge
            all_data = dfs_dict[df_keys[0]]
            for df_key in df_keys[1:]:
                all_data = pd.merge(left=all_data, right=dfs_dict[df_key], on="Timestamp", how='outer')

            # fill NAN with Zero
            all_data.fillna(0, inplace=True)
            # sorting
            all_data.sort_values(by=["Timestamp"], inplace=True, ignore_index=True)
            label_suffix_columns = [f"{col}_{df_key}" for col in label for df_key in df_keys]
            X = all_data.drop(columns=['Timestamp'])
            y = all_data[label_suffix_columns] 

            X_scaled = scaler.transform(X.to_numpy())
            y_scaled = scaler_label.transform(y.to_numpy())

            X_scaled_tensor = torch.tensor(X_scaled).float().to(device)
            y_tensor = torch.tensor(y_scaled).float().view(-1, ue_nums).to(device)  # 將目標轉換為正確的形狀

            if i!=0:
                _, X_scaled_tensor, _, y_tensor = train_test_split(X_scaled_tensor, y_tensor, test_size=0.33, shuffle=False)

            sequences = self.create_inout_sequences(X_scaled_tensor, y_tensor, window_size)
            sequences_list.append(sequences)       

        sequences = self.mix_sequences(sequences_list)

        test_loader = DataLoader(dataset=sequences, batch_size=1, shuffle=False)


        print("The global model status is " + model_type)
        global_model = LSTMModel(input_size=len(features)*ue_nums, hidden_size=hidden_size, num_layers=num_layers, output_size=len(label_suffix_columns)).to(device)
        # loading global model to eval
        model_ndarray_list = np.load(model_path, allow_pickle=True)
        params_dict = zip(global_model.state_dict().keys(), model_ndarray_list)
        state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
        global_model.load_state_dict(state_dict, strict=True)
        global_model.eval()
        
        criterion = nn.MSELoss()
            
        actuals = []
        predictions = []
        pretrained_predictions = []
        finetuned_predictions = []
        # timestamps = all_data['Timestamp'].values[window_size:]  # Skip initial windows

        # pretrained_loss = 0
        with torch.no_grad():
            for i, (seq, labels) in enumerate(test_loader):
                seq = seq.to(device).float().view(-1, window_size, len(features)*ue_nums)
                labels = labels.to(device).float()

                output = global_model(seq)
                global_loss = criterion(output, labels)
                global_loss += global_loss.item()
                global_output_converted = scaler_label.inverse_transform(output.cpu().numpy())[0]
                # pretrained_output = pretrained_model(seq)
                # finetuned_output = finetuned_model(seq)
                # pretrained_loss = criterion(pretrained_output, labels)
                # finetuned_loss = criterion(finetuned_output, labels)
                # pretrained_loss += pretrained_loss.item()
                # finetuned_loss += finetuned_loss.item()
                # pretrained_output_converted = scaler_label.inverse_transform(pretrained_output.cpu().numpy())[0]
                # finetuned_output_converted = scaler_label.inverse_transform(finetuned_output.cpu().numpy())[0]
                label_converted = scaler_label.inverse_transform(labels.cpu().numpy())[0]

                # timestamp = timestamps[i]
                # print(f'Timestamp: {timestamp}, Pre-trained Prediction: {pretrained_output_converted}, Fine-tuned Prediction: {finetuned_output_converted}, Actual: {label_converted}')

                actuals.append(label_converted)
                predictions.append(global_output_converted)
                # pretrained_predictions.append(pretrained_output_converted)
                # finetuned_predictions.append(finetuned_output_converted)

            print(f'Current path: {bs_path}')
            # print(f'Test RMSE: {rmse:.4f}')
            print(f'Number of samples: {len(actuals)}')

        for show_metric in show_metrics:
            # get predict for every UE
            total_actual = []
            total_actual_at_global = []
            # total_actual_at_prtrained = []
            # total_actual_at_finetuned = []
            total_global_predictions = []
            # total_pretrained_predictions = []
            # total_finetuned_predictions = []
            
            actual_ue_data = {}
            global_ue_data = {}
            # pretrained_ue_data = {}
            # finetuned_ue_data = {}
            bs_metrics = {}
            # fig, axs = plt.subplots(2, 2, figsize=(16,9))
            for i in range(len(actuals[0])):
                ue_actuals = [time_stamp[i] for time_stamp in actuals]
                ue_global_predictions = [time_stamp[i] for time_stamp in predictions]
                # ue_pretrained_predictions = [time_stamp[i] for time_stamp in pretrained_predictions]
                # ue_finetuned_predictions = [time_stamp[i] for time_stamp in finetuned_predictions]
                
                time_steps = np.arange(len(ue_actuals))*0.25
                # csv_file_num, model num
                
                if model_type == "pretrained":
                    index = int(len(ue_actuals) * 0.33)
                else:
                    index = int(len(ue_actuals) * 0.67)
                  
                # pretrained_index = int(len(ue_actuals) * 0.33)
                # finetuned_index = int(len(ue_actuals) * 0.67)

                split_actuals_at_global = ue_actuals[index:]
                # split_actuals = ue_actuals[pretrained_index:]
                # split_actuals_at_pretrained = ue_actuals[pretrained_index:]

                split_global_predictions = ue_global_predictions[index:]
                # split_pretrained_predictions = ue_pretrained_predictions[pretrained_index:]
                # split_actuals_at_finetuned = ue_actuals[finetuned_index:]
                # split_finetuned_predictions = ue_finetuned_predictions[finetuned_index:]

                global_time_steps = index * 0.25 + np.arange(len(split_global_predictions)) * 0.25
                # actuals_time_steps = pretrained_index*0.25 + np.arange(len(split_actuals))*0.25
                # pretrained_time_steps =  pretrained_index*0.25 + np.arange(len(split_pretrained_predictions))*0.25
                # finetuned_time_steps =  finetuned_index*0.25 + np.arange(len(split_finetuned_predictions))*0.25

                # ax = axs[i // 2, i % 2]
                if show_mode == "all":
                    total_actual.append(ue_actuals)
                    total_actual_at_global.append(split_actuals_at_global) 
                    total_global_predictions.append(split_global_predictions)
                    # total_pretrained_predictions.append(split_pretrained_predictions)
                    # total_finetuned_predictions.append(split_finetuned_predictions)
                    # total_actual_at_prtrained.append(split_actuals_at_pretrained)
                    # total_actual_at_finetuned.append(split_actuals_at_finetuned)

                    # metrics
                    # front_pretrained_metrics = calculate_metrics(split_actuals_at_pretrained[:finetuned_index-pretrained_index-1], split_pretrained_predictions[:finetuned_index-pretrained_index-1])
                    # back_pretrained_metrics = calculate_metrics(split_actuals_at_pretrained[finetuned_index-pretrained_index-1:], split_pretrained_predictions[finetuned_index-pretrained_index-1:])
                    # finetuned_metrics = calculate_metrics(split_actuals_at_finetuned , split_finetuned_predictions)

                    if show_metric=="total_usage":
                        ue_actuals = [sum(ue_actuals[:i+1]) for i in range(len(ue_actuals))]
                        split_global_predictions = [ue_actuals[index] + sum(split_global_predictions[:i+1]) for i in range(len(split_global_predictions))]
                        # split_pretrained_predictions = [ue_actuals[pretrained_index] + sum(split_pretrained_predictions[:i+1]) for i in range(len(split_pretrained_predictions))]
                        # split_finetuned_predictions = [ue_actuals[finetuned_index]+sum(split_finetuned_predictions[:i+1]) for i in range(len(split_finetuned_predictions))]
                            
                    # plt
                    # ax.plot(time_steps, ue_actuals, label='Ground Truth')  
                    # ax.plot(pretrained_time_steps, split_pretrained_predictions, label='Pre-trained Predicted', alpha=0.5)
                    # ax.plot(finetuned_time_steps, split_finetuned_predictions, label='Fine-tuned Predicted', alpha=0.4)
                    # ax.axvline(x=pretrained_index*0.25, color='y', linestyle='--', linewidth=1)
                    # ax.axvline(x=finetuned_index*0.25, color='g', linestyle='--', linewidth=1)

                    # to_csv
                    actual_ue_data[f'UE{i+1}'] = ue_actuals
                    global_ue_data[f'UE{i+1}'] = [split_actuals_at_global, split_global_predictions]
                    # pretrained_ue_data[f'UE{i+1}']=[split_actuals_at_pretrained, split_pretrained_predictions]
                    # finetuned_ue_data[f'UE{i+1}']=[split_actuals_at_finetuned, split_finetuned_predictions]

                    # metrics = {"front_pretrained":front_pretrained_metrics, "back_pretrained":back_pretrained_metrics, "finetuned":finetuned_metrics}
                    # bs_metrics[f'UE{i+1}'] = metrics

                # set title
                # set_plt_title(f'UE {i+1}', show_metric, front_pretrained_metrics, back_pretrained_metrics, finetuned_metrics, ax)
                # set label
                # ax.set_xlabel('Seconds')
                # ax.set_ylabel('tx_brate downlink [Mbps]')
                # if show_metric != "total_usage":
                    # ax.set_ylim(-0.1, 1)

            actual_data = {
                'timestep': time_steps,
                'ue_data': actual_ue_data
            }

            global_data = {
                'timestep': global_time_steps,
                'ue_data': global_ue_data
            }

            # pretrained_data = {
            #     'timestep': pretrained_time_steps,
            #     'ue_data': pretrained_ue_data
            # }

            # finetuned_data = {
            #     'timestep': finetuned_time_steps,
            #     'ue_data': finetuned_ue_data
            # }

            self.data_to_csv(actual_data, global_data, model_type, path=os.path.join(result_folder_path, 'csv_files'), filename='output.csv', bs_id=bs_list[0])
            # metrics_to_json(metrics=bs_metrics, path=os.path.join(result_folder_path, 'csv_files'), filename='metrics', bs_id=bs_list[0])
            # ax = axs[1, 1]
            # aggregate plt
            # if show_mode == "all":
            #     # all
            #     total_actual = [sum(sublist[i] for sublist in total_actual) for i in range(len(total_actual[0]))]
            #     total_pretrained_predictions = [sum(sublist[i] for sublist in total_pretrained_predictions) for i in range(len(total_pretrained_predictions[0]))]
            #     total_finetuned_predictions = [sum(sublist[i] for sublist in total_finetuned_predictions) for i in range(len(total_finetuned_predictions[0]))]
            #     total_actual_at_prtrained = [sum(sublist[i] for sublist in total_actual_at_prtrained) for i in range(len(total_actual_at_prtrained[0]))]
            #     total_actual_at_finetuned = [sum(sublist[i] for sublist in total_actual_at_finetuned) for i in range(len(total_actual_at_finetuned[0]))]
        
            #     # metrics
            #     front_pretrained_metrics = calculate_metrics(total_actual_at_prtrained[:finetuned_index-pretrained_index-1], total_pretrained_predictions[:finetuned_index-pretrained_index-1])
            #     back_pretrained_metrics = calculate_metrics(total_actual_at_prtrained[finetuned_index-pretrained_index-1:], total_pretrained_predictions[finetuned_index-pretrained_index-1:])
            #     finetuned_metrics = calculate_metrics(total_actual_at_finetuned, total_finetuned_predictions)

            #     if show_metric=="total_usage":
            #         total_actual = [sum(total_actual[:i+1]) for i in range(len(total_actual))]
            #         total_pretrained_predictions = [total_actual[pretrained_index] + sum(total_pretrained_predictions[:i+1]) for i in range(len(total_pretrained_predictions))]
            #         total_finetuned_predictions = [total_actual[finetuned_index] + sum(total_finetuned_predictions[:i+1]) for i in range(len(total_finetuned_predictions))]

                # plt.axvline(x=pretrained_index*0.25, color='g', linestyle='--', linewidth=1, label='pre-trained | fine-tuned ')
                # plt.axvline(x=finetuned_index*0.25, color='y', linestyle='--', linewidth=1, label='fine-tuned | testing(mix sequences) ')
                # ax.plot(time_steps, total_actual , label='Ground Truth')  
                # ax.plot(pretrained_time_steps, total_pretrained_predictions , label='Pre-trained Predicted', alpha=0.5)  
                # ax.plot(finetuned_time_steps, total_finetuned_predictions , label='Fine-tuned Predicted', alpha=0.4)  

            # set title
            # set_plt_title(f"BS{bs_list[0]}", show_metric, front_pretrained_metrics, back_pretrained_metrics, finetuned_metrics, ax)

            # plt.suptitle(f'Pretrained Model: {pretrained_model_path.split("/")[-1]} / Finetuned Model: {finetuned_model_path.split("/")[-1]} / Window Size: {window_size} / Fedprox_mu: {fedprox_mu} / LSTM layers: {num_layers} ')
            # plt.tight_layout()
            # plt.legend(loc="lower left")
            # if show_metric=="total_usage":
                # _, ymax = ax.get_ylim()
                # for ax in axs.flatten():
                    # ax.set_ylim(0, ymax)
            # plt.savefig(os.path.join(result_folder_path, f'mix/mix_sequence_{show_metric}_prediction_result'))
            # plt.show()
            # plt.close(fig)

    def eval(self, file):   
        # load training config
        #training_config_path = "/hcds_vol/private/yanhong/training_config.yaml"
        # print(file)
        config = self.load_yaml(file)
        # print(config)

        # # Centralized
        # X_scaler_path = os.path.join(result_folder_path, "scaler/X_scaler.save")
        # y_scaler_path = os.path.join(result_folder_path, "scaler/y_scaler.save")
        # pretrained_model_path = os.path.join(result_folder_path, "slice{}_best_pretrained_model.pth".format(slice_id))
        # # finetuned_model_path =  os.path.join(result_folder_path, "slice{}_best_finetuned_model.pth".format(slice_id))
        # # FL
        # # X_scaler_filename = os.path.join(result_folder_path, "scaler/fl_X_scaler.save")
        # # y_scaler_filename = os.path.join(result_folder_path, "scaler/fl_y_scaler.save")
        # # pretrained_result_folder_path = os.path.join(result_folder_path, slice0_fl_best_pretrained_global_model.pth)
        # finetuned_model_path =  os.path.join(result_folder_path, "slice{}_fl_best_finetuned_global_model.pth".format(slice_id))

        X_scaler_path = config['X_scaler_path']
        y_scaler_path = config['y_scaler_path']
        model_path = config['model_path']
        # pretrained_model_path = config['pretrained_model_path']
        # finetuned_model_path =  config['finetuned_model_path']

        # current_directory = os.getcwd()

        # # 打印当前工作目录
        # print("Current working directory:", current_directory)
        self.test_mix(
            config=config,
            X_scaler_path=X_scaler_path,
            y_scaler_path=y_scaler_path,
            model_path = model_path
            # pretrained_model_path=pretrained_model_path,
            # finetuned_model_path=finetuned_model_path,
        )

# def main():
#     test = Test_model()
#     test.eval(file = '/hcds_vol/private/yanhong/training_config.yaml')

# if __name__ == "__main__":
#     main()