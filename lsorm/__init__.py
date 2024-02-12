from sqlalchemy import URL, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class SessionMaker(sessionmaker):
    def configure(self, **kwargs):
        engine = None
        source = kwargs.pop("source", None)

        # Decide the order based on the 'source' argument
        if source.lower() in ("settings", "settings_file"):
            engine = self.configure_settings_file()

        elif source.lower() in ("env", "e", "env_variables"):
            engine = self.configure_env_variables()
        elif source.lower() in ("config", "conf_file", "conf", "config_file"):
            engine = self.configure_config_file(**kwargs)
        else:
            # Default order: settings -> env -> config
            engine = (
                self.configure_settings_file()
                or self.configure_env_variables()
                or self.configure_config_file()
            )

        if engine is not None:
            super().configure(bind=engine, **kwargs)
        else:
            raise ValueError("Failed to configure engine from any source")

    def configure_settings_file(self):
        try:
            print("IMPORTING SETTINGS FILE ")
            import settings

            name = settings.DB_NAME
            type = settings.DB_TYPE
            username = settings.DB_USERNAME
            password = settings.DB_PASSWORD
            host = settings.DB_HOST

            engine = self._create_engine(type, username, password, host, name)

            return engine
        except:
            # TODO: add catch here
            return None

    def configure_env_variables(self):
        try:
            import os

            name = os.environ.get("DB_NAME")
            type = os.environ.get("DB_TYPE")
            username = os.environ.get("DB_USERNAME")
            password = os.environ.get("DB_PASSWORD")
            host = os.environ.get("DB_HOST")

            engine = self._create_engine(type, username, password, host, name)
            return engine
        except:
            # TODO: add catch
            return None

    def configure_config_file(self, **kwargs):
        """
        Specify config_file path
        """
        try:
            import yaml

            config_file = kwargs.get("config_file")
            with open(config_file, "r") as file:
                config = yaml.safe_load(file)

                type = config.get("database").get("type")
                username = config.get("database").get("username")
                password = config.get("database").get("password")
                host = config.get("database").get("host")
                name = config.get("database").get("name")
                engine = self._create_engine(
                    type, username, password, host, name
                )
            return engine
        except KeyError:
            return None
        except yaml.YAMLError as e:
            raise RuntimeError(f"Error parsing configuration file: {e}")
        # TODO: Make this more robust

    def _create_engine(self, type, username, password, host, name):
        url_object = URL.create(
            type,
            username=username,
            password=password,  # plain (unescaped) text
            host=host,
            database=name,
        )
        engine = create_engine(url=url_object)
        return engine


Session = scoped_session(SessionMaker())
