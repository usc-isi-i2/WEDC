from wedc.domain.core.ml.classifier.label_propagation import labelprop



def map_labelprop(iterator):
    # for key, vector in iterator:
    yield labelprop.run(list(iterator))