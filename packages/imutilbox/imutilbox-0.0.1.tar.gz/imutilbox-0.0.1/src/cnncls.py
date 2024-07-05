import os
import datetime
import uuid
import numpy as np
import torch
from imutilbox import DataClass


class CLSCORE():
    """A class provides training and inference functions for a classification model

    CLSCORE is a class that provides training and inference functions for a classification model.
    It requires a model, a data class, and a temporary directory path to save intermediate checkpoints and training logs automatically.

    Args:
        model (torch.nn.Module): a model to be trained
        dataclass (DataClass): a data class that contains class labels
        temp_dirpath (str): a temporary directory path to save intermediate checkpoints and training logs

    Attributes:
        device (str): a device to run the model
        dataclass (DataClass): a data class that contains class labels
        model (torch.nn.Module): a model to be trained
        temp_dirpath (str): a temporary directory path to save intermediate checkpoints and training logs
        train_stats (dict): a dictionary to save training statistics
        test_stats (dict): a dictionary to save test statistics

    Examples:
        >>> import torch
        >>> import torchvision
        >>> from imutilbox import DataClass
        >>>
        >>> # dataset
        >>> dataclass = DataClass('dataclass.txt')
        >>> dataloaders = {
        >>>     'train': train_dataloader,
        >>>     'valid': valid_dataloader,
        >>>     'test': test_dataloader
        >>> }
        >>>
        >>> # model
        >>> model = torchvision.models.efficientnet_b7(
        >>>     weights=torchvision.models.EfficientNet_B7_Weights.DEFAULT)
        >>> model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, len(dataclass.classes))
        >>>
        >>> # train and inference
        >>> clscore = CLSCORE(model, dataclass)
        >>> clscore.train(dataloaders, epochs=20, lr=0.01)
        >>>
        >>> dataloader = test_dataloader
        >>> probs = clscore.inference(dataloader)
    """

    def __init__(self, model, dataclass, temp_dirpath=None):
        # device
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        # data class
        if isinstance(dataclass, str):
            dataclass = DataClass(dataclass)
        elif not isinstance(dataclass, DataClass):
            raise TypeError('Invalid type: {}'.format(type(dataclass)))
        self.dataclass = dataclass

        # model
        self.model = model
        self.model = self.model.to(self.device)
        
        # create variables to save intermediate checkpoints and training logs
        self.temp_dirpath = self.__init_tempdir(temp_dirpath)
        self.train_stats = {
            'epoch': [],
            'train_loss': [],
            'train_acc': [],
            'valid_loss': [],
            'valid_acc': []
        }
        self.test_stats = None

    
    def __init_tempdir(self, temp_dirpath):
        if temp_dirpath is None:
            temp_dirpath = os.path.join(
                os.getcwd(),
                '{}_{}'.format(str(uuid.uuid4()).replace('-', '')[0:8],
                              datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        if not os.path.exists(temp_dirpath):
            os.makedirs(temp_dirpath)
        return temp_dirpath


    def train(self, dataloaders, epochs=20,  lr=0.01, resume=False):
        """Train the model with the provided dataloaders

        Train the model with the provided dataloaders. The training statistics are saved in the temporary directory.

        Args:
            dataloaders (dict): a dictionary of dataloaders for training, validation, and test
            epochs (int): the number of epochs to train the model
            lr (float): the learning rate for the optimizer
            resume (bool): resume training from the last checkpoint if True
        
        Examples:
            >>> import torch
            >>> import torchvision
            >>> from imutilbox import DataClass
            >>>
            >>> # dataset
            >>> dataclass = DataClass
            >>> dataloaders = {
            >>>     'train': train_dataloader,
            >>>     'valid': valid_dataloader,
            >>>     'test': test_dataloader
            >>> }
            >>>
            >>> # model
            >>> model = torchvision.models.efficientnet_b7(
            >>>     weights=torchvision.models.EfficientNet_B7_Weights.DEFAULT)
            >>> model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, len(dataclass.classes))
            >>>
            >>> # train
            >>> clscore = CLSCORE(model, dataclass)
            >>> clscore.train(dataloaders, epochs=20, lr=0.01)
        """

        # training params
        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(self.model.parameters(), lr=lr)
        
        # set up train/validation datasets
        if 'train' not in dataloaders:
            raise ValueError('train dataset is not provided')

        # resume training from the last checkpoint if resume is True
        last_epoch = 0
        if resume:
            last_epoch = self.__update_model_weight()

        # train the model
        for epoch in range(last_epoch + 1, epochs + 1):
            print(f'Epoch {epoch}/{epochs}')

            # training and validation
            self.train_stats['epoch'].append(epoch)
            for phase in ['train', 'valid']:
                loss, acc, probs = self.__train(dataloaders[phase], criterion, optimizer, phase)
                self.train_stats[f'{phase}_loss'].append(loss)
                self.train_stats[f'{phase}_acc'].append(acc)
                if loss is not None and acc is not None:
                    print(f'{phase} loss: {loss:.4f}, acc: {acc:.4f}')

            # test the model if dataset is provided at the last epoch
            if epoch == epochs and dataloaders['test'] is not None:
                loss, acc, probs = self.__train(dataloaders['test'], criterion, optimizer, phase)
                self.test_stats = {
                    'dataset': dataloaders['test'].dataset,
                    'loss': loss,
                    'acc': acc,
                    'probs': probs
                }
            
            self.save(os.path.join(self.temp_dirpath, f'checkpoint_latest.pth'))



    def __update_model_weight(self):
        last_epoch = 0

        trainstats_fpath = os.path.join(self.temp_dirpath, 'train_stats.txt')
        chk_fpath = os.path.join(self.temp_dirpath, 'checkpoint_latest.pth')
        if os.path.exists(trainstats_fpath) and os.path.exists(chk_fpath):
            # update train stats
            with open(trainstats_fpath, 'r') as fh:
                tags = fh.readline().strip().split('\t')
                for tag in tags:
                    self.train_stats[tag] = []
                for f_line in fh:
                    vals = f_line.strip().split('\t')
                    for tag, val in zip(tags, vals):
                        if val is not None:
                            if val != 'NA' and val != 'None':
                                if tag == 'epoch':
                                    val = int(val)
                                else:
                                    val = float(val)
                        self.train_stats[tag].append(val)
            # update model weight with the last checkpoint
            self.model = self.model.to('cpu')
            self.model.load_state_dict(torch.load(chk_fpath))
            self.model = self.model.to(self.device)
            last_epoch = max(self.train_stats['epoch'])
            
        return last_epoch



    def __train(self, dataloader, criterion, optimizer, phase):
        if dataloader is None:
            return None, None, None
        if phase == 'trian':
            self.model.train()
        else:
            self.model.eval()

        running_loss = 0.0
        running_corrects = 0
        probs = []

        for inputs, labels in dataloader:
            inputs = inputs.to(self.device)
            labels = labels.to(self.device)

            optimizer.zero_grad()
            with torch.set_grad_enabled(phase == 'train'):
                outputs = self.model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)

                if phase == 'train':
                    loss.backward()
                    optimizer.step()

            #running_loss += loss.item() * inputs.size(0)
            running_loss += loss * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            probs.append(torch.nn.functional.softmax(outputs, dim=1).detach().cpu().numpy())

        epoch_loss = running_loss.double().item() / len(dataloader.dataset)
        epoch_acc = running_corrects.double().item() / len(dataloader.dataset)
        probs = np.concatenate(probs, axis=0).tolist()
        return epoch_loss, epoch_acc, probs



    def __str(self, s):
        if s is None:
            return 'NA'
        return str(s)


    def __write_train_stats(self, output_log_fpath):
        with open(output_log_fpath, 'w') as fh:
            fh.write('\t'.join(self.train_stats.keys()) + '\n')
            for vals in zip(*self.train_stats.values()):
                fh.write('\t'.join([self.__str(v) for v in vals]) + '\n')


    def __write_test_outputs(self, output_log_fpath):
        with open(output_log_fpath, 'w') as fh:
            fh.write('# loss: {}\n'.format(self.test_stats['loss']))
            fh.write('# acc: {}\n'.format(self.test_stats['acc']))
            fh.write('\t'.join(['image', 'label'] + self.dataclass.classes) + '\n')
            for x_, y_, p_ in zip(self.test_stats['dataset'].x, self.test_stats['dataset'].y, self.test_stats['probs']):
                y_ = self.dataclass.classes[y_]
                fh.write(f'{x_}\t{y_}\t{p_[0]}\t{p_[1]}\n')


    def save(self, output_fpath):
        """Save the model and training statistics

        Save the model and training statistics in the provided output file path. The output file path should end with '.pth'.

        Args:
            output_fpath (str): an output file path to save the model and training statistics
        """
        if not output_fpath.endswith('.pth'):
            output_fpath += '.pth'
        self.model = self.model.to('cpu')
        torch.save(self.model.state_dict(), output_fpath)
        self.model = self.model.to(self.device)

        output_log_fpath = os.path.splitext(output_fpath)[0] + '.train_stats.txt'
        self.__write_train_stats(output_log_fpath)

        if self.test_stats is not None:
            output_log_fpath = os.path.splitext(output_fpath)[0] + '.test_outputs.txt'
            self.__write_test_outputs(output_log_fpath)


    def inference(self, dataloader):
        """Inference the model with the provided dataloader

        Inference the model with the provided dataloader. The output is a list of probabilities for each class.

        Args:
            dataloader (torch.utils.data.DataLoader): a dataloader for inference
        """
        self.model = self.model.to(self.device)
        self.model.eval()

        probs = []
        for inputs in dataloader:
            inputs = inputs.to(self.device)
            with torch.set_grad_enabled(False):
                outputs = self.model(inputs)
            probs.append(torch.nn.functional.softmax(outputs, dim=1).detach().cpu().numpy())

        probs = np.concatenate(probs, axis=0).tolist()
        return probs

