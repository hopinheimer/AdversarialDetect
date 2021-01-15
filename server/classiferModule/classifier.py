import matplotlib as plt
import torchvision
from PIL import Image
import torch
from torchvision import models
import torchvision.transforms.functional as TF
import torch.nn.functional as F
import torchvision.transforms as T


class detect(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = torch.nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1, stride=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 3, kernel_size=3, padding=1, stride=1),
            nn.BatchNorm2d(3),
            nn.ReLU()
        )
        self.linear1 = nn.Linear(14*14*3, 128)
        self.relu1 = nn.ReLU()
        self.linear2 = nn.Linear(128, 1)

    def forward(self, xb):
        x = self.conv1(xb)
        x = x.view(xb.size(0), -1)
        x = self.linear1(x)
        x = self.relu1(x)
        x = self.linear2(x)
        x = torch.sigmoid(x)
        return x

    def training_step(self, batch):
        x, l = batch
        out = self(x)
        out = torch.squeeze(out, 1).type(torch.float32)
        l = l.type(torch.float32)
        loss = F.binary_cross_entropy(out, l)
        return loss

    def test_step(self, batch):
        x, l = batch
        out = self(x)
        out = torch.squeeze(out, 1).type(torch.float32)
        l = l.type(torch.float32)
        loss = F.binary_cross_entropy(out, l)
        acc = accuracy(out, l)
        return {'test_loss': loss.detach().item(), 'test_acc': acc.item()}


model = torch.load('./models/model.pt')
model.eval()


def classifierFunc():
    image_size = 28
    dataset = torchvision.datasets.ImageFolder('../server/uploads', transform=torchvision.transforms.Compose(
        [T.Resize((image_size, image_size), interpolation=Image.NEAREST), T.ToTensor()]))

    test_loader = torch.utils.data.DataLoader(dataset)
    for image, l in test_loader:

        out = model.forward(image)      # Model predictions
        print(out)
        # Model prediction shape


classifierFunc()
