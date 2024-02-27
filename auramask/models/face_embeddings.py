from enum import Enum
from deepface.DeepFace import build_model
import tensorflow as tf
# from keras_cv.layers import Resizing

class FaceEmbedEnum(str, Enum):
  VGGFACE = "VGG-Face"
  FACENET = "Facenet"
  FACENET512 = "Facenet512"
  OPENFACE = "OpenFace"
  DEEPFACE = "DeepFace"
  DEEPID = "DeepID"
  ARCFACE = "ArcFace"
  SFACE = "SFace"
  def get_model(self):
    model = build_model(model_name=self.value)
    shape = model.input_shape[::-1]
    # aug = Resizing(shape[0], shape[1])
    model = model.model
    model._name = self.name
    model.trainable = False
    for layer in model.layers:
      layer.trainable = False
      layer._name = "%s/%s"%(model.name, layer.name)
    return (model, shape, self.name.lower())
  @classmethod
  def build_F(cls, targets: list):
    F = set()
    for model_label in targets:
      assert model_label in cls
      F.add(
        model_label.get_model()
      )
    return F
  def toJSON(self):
    return self.name