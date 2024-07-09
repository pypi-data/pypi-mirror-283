import torch
import torch.nn as nn

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size, is_finetuned=False):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        # self.leaky_relu = nn.LeakyReLU(negative_slope=0.01)

        #Freeze the first two layers of the LSTM
        if is_finetuned:
            for param_name, param in self.lstm.named_parameters():
                layer_num = int(param_name.split('_')[2][1])  # layer number is in the parameter name, e.g., weight_ih_l0
                if layer_num < 0:  # freeze the layer
                    param.requires_grad_(False)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        # out = self.leaky_relu(out)
        return out