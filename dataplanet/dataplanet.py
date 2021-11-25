class dataplanet:

    def __init__(self, experiment_name, param_list, metric_list):
        self.dataverse_url = "http://dataverse-dev.localhost:8085"
        self.experiment_name = experiment_name
        self.param_list = param_list
        self.metric_list = metric_list

    def set_tracking_uri(self, tracking_uri):
        self.tracking_uri = tracking_uri
        mlflow.set_tracking_uri(self.tracking_uri)

    def set_dataverse_url(self, dataverse_url):
        self.dataverse_url = dataverse_url

    def get_dataverse_url(self):
        return self.dataverse_url

    def set_param_list(self, *param_list):
        self.param_list = param_list
        log_params(param_list)

    def get_param_list(self):
        return self.param_list

    def set_metric_list(self, *metric_list):
        self.metric_list = metric_list
        log_metrics(metric_list)

    def get_metric_list(self):
        return self.metric_list

    def set_experiment_name(self, experiment_name):
        self.experiment_name = experiment_name
        mlflow.set_experiment(self.experiment_name)

    def get_experiment_name(self):
        return self.experiment_name

    def get_model(self):
        return self.model

    def get_models(self):
        models=[]
        for ri in mlflow.list_run_infos(mlflow.get_experiment_by_name(self.experiment_name)):
            run = mlflow.get_run(ri.run_id)
            for metric in metric_list:
                try:
                    m = run.data.metrics[metric]
                    artifact_uri = run.info.artifact_uri
                    models.append((artifact_uri,metric))
                except KeyError:
                    pass
        return models

    def log_metrics(self):
        for metric in self.metric_list:
            if metric == 'accuracy':
                mlflow.log_metric(metric, accuracy_score(self.labels, self.predictions))

    def log_params(self, *param_values):
        values = iter(param_values)
        for param in self.param_list:
            mlflow.log_param(param, next(values))

    def start_run(self):
        mlflow.start_run()

    def get_model_signature(self, features, predictions):
        self.model_signature = infer_signature(features, predictions)
        return self.model_signature

    def set_model_signature(self, model_signature):
        self.model_signature = model_signature

    def log(self, labels, predictions):
        self.predictions = predictions
        self.labels = labels
        log_metrics()

    def set_param_count(self):
        self.param_count = len(self.param_list)

    def get_param_count(self):
        return self.param_count

    def set_model_library(self, model):
        self.model_library = str(type(model)).split('.')[0].split('\'')

    def get_model_library(self):
        return self.model_library