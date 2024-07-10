from pymerkle import InmemoryTree as MerkleTree


class ModelMetadata:
    def __init__(
        self,
        model_name,
        model_md5,
        model_url,
        dataset_url,
        training_params=None,
        training_date=None,
        model_version=None,
        author=None,
        description=None,
        dataset_params=None,
        merkle_root=None,
    ):
        """
        Initialize model metadata.

        :param model_name: The name of the model.
        :param model_md5: The MD5 hash of the model, used to uniquely identify the model.
        :param model_url: The URL where the trained model is stored.
        :param dataset_url: The URL of the dataset used to train the model.
        :param training_params: Parameters used for training the model, such as number of epochs, batch size, etc.
        :param training_date: The date when the model was trained.
        :param model_version: The version of the model, used to track model iterations.
        :param author: The author or entity that trained the model.
        :param description: A brief description of the model, including its purpose and other relevant information.
        :param dataset_params: Parameters of the dataset used for training the model.
        :param merkle_root: The Merkle root of the metadata fields.
        """
        self.model_md5 = model_md5
        self.model_name = model_name
        self.model_url = model_url
        self.dataset_url = dataset_url
        self.training_params = training_params
        self.training_date = training_date
        self.model_version = model_version
        self.author = author
        self.description = description
        self.dataset_params = dataset_params
        self.protocol_version = "1.0.0"

        if merkle_root:
            # Use the provided Merkle root
            self.merkle_root = merkle_root
        else:
            # Generate a Merkle tree from the metadata fields
            tree = MerkleTree(algorithm="sha256")
            for field_value in [
                self.model_md5,
                self.model_name,
                self.model_url,
                self.dataset_url,
                self.training_params,
                self.training_date,
                self.model_version,
                self.author,
                self.description,
                self.dataset_params,
                self.protocol_version,
            ]:
                tree.append_entry(str(field_value).encode())

            merkle_root = tree.get_state(tree.get_size())

            # Add the Merkle root to the metadata
            self.merkle_root = merkle_root.hex()

    @classmethod
    def from_dict(cls, data):
        """
        Create a ModelMetadata instance from a dictionary.

        :param data: A dictionary containing model metadata.
        :return: A ModelMetadata instance.
        """
        return cls(
            model_md5=data.get("model_md5"),
            model_name=data.get("model_name"),
            model_url=data.get("model_url"),
            dataset_url=data.get("dataset_url"),
            training_params=data.get("training_params"),
            training_date=data.get("training_date"),
            model_version=data.get("model_version"),
            author=data.get("author"),
            description=data.get("description"),
            dataset_params=data.get("dataset_params"),
            merkle_root=data.get("merkle_root"),  # Set the Merkle root from the dictionary
        )

    def to_dict(self):
        """
        Convert a ModelMetadata instance to a dictionary.

        :return: A dictionary representation of the ModelMetadata instance.
        """
        return {
            "model_md5": self.model_md5,
            "model_name": self.model_name,
            "model_url": self.model_url,
            "dataset_url": self.dataset_url,
            "training_params": self.training_params,
            "training_date": self.training_date,
            "model_version": self.model_version,
            "author": self.author,
            "description": self.description,
            "dataset_params": self.dataset_params,
            "protocol_version": self.protocol_version,
            "merkle_root": self.merkle_root,
        }
