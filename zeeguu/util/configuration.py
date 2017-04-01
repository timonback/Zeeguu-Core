import os


def assert_configs(config, required_keys, config_file_name):
    for key in required_keys:
        config_value = config.get(key, None)
        if config_value is None:
            print "Please define the {key} key in the {config} file!".format(key=key, config=config_file_name)
            exit(-1)


def load_configuration_or_abort(app, environ_variable, mandatory_config_keys):
    """
    
        Try to load config from the file named in the environ variable. 
                
        If a config is loaded, the function makes sure that the mandatory_config_keys are 
        in the file
        
    :return: Returns in case of success. Throws exception otherwise. 

    """

    try:
        config_file = os.environ[environ_variable]
        app.config.from_pyfile(config_file, silent=False)
        assert_configs(app.config, mandatory_config_keys, config_file)
        print ("Successfully loaded zeeguu config from {0}".format(config_file))
        return
    except Exception as e:

        raise Exception(
            "You must define a {0} environment var to be able to load the configuration. "
            .format(environ_variable))