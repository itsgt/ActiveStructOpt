from activestructopt.model.base import BaseModel
from activestructopt.common.registry import registry
from activestructopt.dataset.base import BaseDataset
import torch

@registry.register_model("GroundTruth")
class GroundTruth(BaseModel):
  def __init__(self, config, simfunc, **kwargs):
    self.simfunc = simfunc

  def train(self, dataset: BaseDataset, **kwargs):
    return None, None, torch.empty(0)

  def predict(self, structure, **kwargs):
    self.simfunc.get(structure)
    gt = self.simfunc.resolve()
    unc = torch.zeros(gt.size())

    return torch.stack((gt, unc))
