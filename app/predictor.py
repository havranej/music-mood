import torch
from torch import nn
from torch.nn import functional as F

import os

MEANS = torch.Tensor([ 9.6994e-02,  3.8720e-02,  3.1402e+00,  1.8772e-01,  2.0566e-01,
          8.0149e-01,  8.7217e-03,  1.5696e-01, -2.4529e+01,  2.2588e+00,
          3.1217e-02,  2.8291e-01, -6.0957e-03,  9.5511e-02, -3.1094e-02,
          4.6710e-02, -1.9522e-02,  2.3542e-02, -1.5204e-02,  1.9254e-02,
         -1.4686e-03,  1.8226e-02,  6.4972e-03,  4.8800e-02,  1.2898e-02,
          2.2536e-02,  1.2507e-02,  5.4475e-02,  2.6495e-03,  6.7312e-03,
          1.5743e-02,  3.7801e-02,  5.5788e-03,  3.3670e-02,  8.7435e-05,
          3.7929e-05,  2.6858e-03, -1.6662e-06, -1.0416e-05, -2.7250e-05,
          1.2390e-05,  7.5020e-06,  8.0157e-03,  1.1057e-04,  1.2809e-04,
          6.2925e-05, -3.9527e-06,  2.1396e-05, -3.6802e-05,  4.5715e-05,
         -4.2590e-05, -1.4666e-05,  2.6423e-05,  1.3444e-05, -4.7650e-06,
          3.2266e-06,  3.7435e-06,  1.1364e-05,  1.3754e-08,  3.0878e-06,
          1.6678e-06,  5.9466e-06, -3.1267e-07, -4.5458e-07,  1.9818e-06,
         -9.4702e-06, -6.9915e-07,  1.3857e-05])

STDS = torch.Tensor([0.0713, 0.0431, 0.2312, 0.0765, 0.0477, 0.6339, 0.0172, 0.1506, 2.8243,
         1.0384, 0.7486, 0.5173, 0.4523, 0.3881, 0.3685, 0.3462, 0.3473, 0.3333,
         0.3175, 0.2899, 0.2695, 0.0315, 0.0173, 0.0619, 0.0242, 0.0323, 0.0247,
         0.0725, 0.0086, 0.0137, 0.0228, 0.0465, 0.0132, 0.0202, 0.0436, 0.0296,
         0.2773, 0.0471, 0.0349, 0.3646, 0.0202, 0.1094, 1.4301, 0.5400, 0.3881,
         0.3317, 0.3003, 0.2782, 0.2679, 0.2599, 0.2548, 0.2489, 0.2428, 0.2320,
         0.2211, 0.0224, 0.0114, 0.0447, 0.0172, 0.0224, 0.0170, 0.0526, 0.0072,
         0.0106, 0.0173, 0.0341, 0.0096, 0.0145])


class Forked_GRU(nn.Module):
    def __init__(self, hidden_size, num_layers = 1, p_dropout = 0, bidirectional = False):
        super(Forked_GRU, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.bidirectional = bidirectional

        self.GRU = nn.GRU(68, hidden_size, num_layers = num_layers, batch_first = True, dropout = p_dropout if num_layers > 1 else 0, bidirectional = bidirectional)
        self.dropout = nn.Dropout(p = p_dropout)

        self.FC1_a = nn.Linear(hidden_size, 5)
        self.FC2_a = nn.Linear(5, 1)

        self.FC1_v = nn.Linear(hidden_size, 5)
        self.FC2_v = nn.Linear(5, 1)

    def forward(self, x):
        x, _ = self.GRU(x)
        x = x[:,-1,:] # Taking the final output only

        x = F.relu(x)
        x = self.dropout(x)

        a = F.relu(self.FC1_a(x))
        a = torch.tanh(self.FC2_a(a)).flatten()

        v = F.relu(self.FC1_v(x))
        v = torch.tanh(self.FC2_v(v)).flatten()
        return a, v


class Ensemble():
    def __init__(self, models = []):
        self.models = models
  
    def predict(self, x):
        a_preds, v_preds = [], []
        for model in self.models:
            a, v = model(x)
            a_preds.append(a)
            v_preds.append(v)
        a_prediction = torch.stack(a_preds).mean(dim = 0)
        v_prediction = torch.stack(v_preds).mean(dim = 0)
        return a_prediction, v_prediction

    def load_models(self, dir, n_models):
        for i in range(n_models):
            model = Forked_GRU(hidden_size = 30, num_layers = 1, p_dropout = 0.25)
            model.load_state_dict(torch.load(os.path.join(dir, f"model{i}.zip"), map_location = torch.device("cpu")))
            model.eval()
            self.models.append(model)

    def predict_from_features(self, features):
        features_tensor = torch.Tensor(features.T)
        features_tensor = features_tensor[None,:,:]
        features_tensor = (features_tensor - MEANS) / STDS
        a_pred, v_pred = self.predict(features_tensor)
        return a_pred.item(), v_pred.item()