from snowflake.ml.registry import Registry
from .snowflakesession import snowflakesession as SnowflakeSession
from .utilities import DatasetManager, Metadata
from fosforml.utils import get_headers
from fosforml.constants import NotebooksAPI
from datetime import datetime
import json,requests
import snowflake

class ModelRegistry:
    def __init__(self,session):
        self.session_instance = SnowflakeSession()
        self.snowflake_session = session
        self.model_registry = Registry(session=self.snowflake_session, 
                                       database_name=self.session_instance.connection_params[0]["connectionDetails"]['defaultDb'],
                                       schema_name=self.session_instance.connection_params[0]["connectionDetails"]['defaultSchema']
                                       )
        self.models_info = self.model_registry.show_models()

    def register_model(self,
                       model,
                       score,
                       model_name,
                       description,
                       conda_dependencies,
                       model_flavour,
                       model_type,
                       x_train,
                       y_train,
                       x_test,
                       y_test,
                       y_pred,
                       prob,
                       python_version,
                       source,
                       metadata
                       ):
        
        if score :
            return False, "Feature is not implemented yet."

        metrics = self.get_model_metrics(source,model,metadata)
        metrics['python_version'] = python_version
        metrics['conda_dependencies'] = str(conda_dependencies)

        model_version = self.get_model_version(self.model_registry,model_name)

        ## register model
        try:
            self.model_registry.log_model(model,
                   model_name=model_name,
                   version_name=model_version,
                   comment=description,
                   conda_dependencies=conda_dependencies,
                   metrics=metrics,
                   sample_input_data=x_train.columns,
                   python_version=python_version  
                  )
        except Exception as e:
            return False,f"Failed to register model '{model_name}'. {str(e)}"
        
        ## upload model datasets
        dataset_manager = DatasetManager(model_name=model_name,
                                         version_name=model_version,
                                         session=self.snowflake_session
                                         )
        ds_status,ds_message = dataset_manager.upload_datasets(
                                session=self.snowflake_session,
                                datasets={
                                        "x_train": x_train,
                                        "y_train": y_train,
                                        "x_test": x_test,
                                        "y_test": y_test,
                                        "y_pred": y_pred,
                                        "prob": prob
                                    })

        if not ds_status:
            return False,ds_message

        ## update model metadata
        metadata = Metadata(model_registry=self.model_registry)
        metadata_status,metadata_message = metadata.update_model_registry(
            session=self.snowflake_session,
            model_name=model_name,
            model_description=description,
            model_tags={
                "FLAVOR": model_flavour,
                "MODELTYPE": model_type,
                "CREATEDON" : metrics['created_on']
            }
        )

        if not metadata_status:
            return False,metadata_message
        
        return True,f"Model '{model_name}' registered successfully."

    def update_model_details(self,
                             model_name,
                             comments,
                             model_tags):
        metadata = Metadata(model_registry=self.model_registry)
        return metadata.update_model_registry(
            session=self.snowflake_session,
            model_name=model_name,
            model_description=comments,
            model_tags=model_tags
        )

    def get_model_details(self, model_name):
        pass

    def get_model_version(self, registry, model_name):
        model_info = registry.show_models()[registry.show_models()['name']==model_name.upper()]
        if model_info.empty:
            return "v1"
        model_versions = json.loads(model_info.versions.to_list()[0])
        if not model_versions:
            return "v1"
        else:
            last_version = max(model_versions,key=lambda x: int(x[1:]),default='v0')
            return f"v{int(last_version[1:])+1}"
    
    def get_model_metrics(self,source,model,metadata):
        metrics = {}
        metrics['model_metrics'] = self.get_model_performance_metrics()
        metrics['hyper_parameters'] = self.get_hyper_parameters(model)
        sourrce_info = self.get_source_details(source)
        metrics['created_on'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
        metrics['created_by'] = self.session_instance.connection_params[0]["connectionDetails"]['dbUserName']
        metrics['status'] = sourrce_info['stauts']
        metrics['source'] = source
        metrics['Repo_Details'] = sourrce_info['repo_details']
        if metadata:
            metrics['metadata'] = json.dumps(metadata)
        
        return metrics

    def get_hyper_parameters(self,model):
        return json.dumps(model.get_params())

    
    def get_model_performance_metrics(self):
        dummy_data = {'{"tag": "feature_importance", "model_metric_value": [{"column_name": "DEPARTMENT", "importance": 0.14061672606947828}, {"column_name": "SATISFACTION_LEVEL", "importance": 0.1104329386548882}, {"column_name": "LAST_EVALUATION", "importance": 0.1350624049528422}, {"column_name": "NUMBER_PROJECT", "importance": 0.04248402957988852}, {"column_name": "AVERAGE_MONTLY_HOURS", "importance": 0.2118735496815215}, {"column_name": "TIME_SPEND_COMPANY", "importance": 0.10658202765565672}, {"column_name": "WORK_ACCIDENT", "importance": 0.010641980974635002}, {"column_name": "LEFT", "importance": 0.16529938539291036}, {"column_name": "PROMOTION_LAST_5YEARS", "importance": 0.0770069570381792}]}', '{"tag": "confusion_matrix", "model_metric_value": [{"column_1_counter": 0, "column_2_counter": 0, "prediction": 1404.0, "column_1": 0, "column_2": 0}, {"column_1_counter": 0, "column_2_counter": 1, "prediction": 380.0, "column_1": 0, "column_2": 1}, {"column_1_counter": 1, "column_2_counter": 0, "prediction": 1129.0, "column_1": 1, "column_2": 0}, {"column_1_counter": 1, "column_2_counter": 1, "prediction": 483.0, "column_1": 1, "column_2": 1}]}', '{"tag": "detailed_matrix", "model_metric_value": {"accuracy_score": 0.555654, "precision_score": 0.5596755504055619, "recall_score": 0.29962779156327546, "f1_score": 0.3903030303030303, "log_loss": 16.01586365258474, "roc_auc_score": 0.5433116536291713}}', '{"tag": "roc_auc", "model_metric_value": {"fpr": [0.0, 0.21300448430493274, 1.0], "tpr": [0.0, 0.29962779156327546, 1.0], "data": 0.5433116536291713}}'}
        return json.dumps(list(dummy_data))
    
    def get_source_details(self,source):
        source_info = {}
        if source == "EXPERIMENT":
            source_info['stauts'] = "Experimented"
        if source == "BYOM":
            source_info['stauts'] = "Deploying"
        if not source or source == "UNKNOWN":
            source_info['stauts'] = "Registered"
        if source == "NOTEBOOK" or source == "" or source is None:
            source_info['stauts'] = "Registered"
            source_info['repo_details'] = self.get_repo_details()
        
        return source_info

    def get_repo_details(self):
        try:
            url = NotebooksAPI.notebooks_api_server_url + NotebooksAPI.git_repo
            headers = get_headers()
            response = requests.get(url, headers=headers).text
            return response
        except Exception as e:
            print(e,"Unable to Fetch Repo Details")
            return ""