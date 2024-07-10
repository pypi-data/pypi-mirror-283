class EventObject:
    requiredParameters = ['gebeurteniscode', 'actiecode', 'utcisodatetime', 'identificatortype', 'identificator', 'aard']
    
    def __init__(self, **eventParameters) -> None:
        # Initialize with default empty values or with provided parameters
        for param in self.requiredParameters:
            setattr(self, param, eventParameters.get(param, None))

    def update_parameters(self, **eventParameters) -> None:
        for param, value in eventParameters.items():
            setattr(self, param, value)

    def validate(self) -> None:
        for param in self.requiredParameters:
            if getattr(self, param) is None:
                raise KeyError(f"Missing required parameter: {param}")

class UserObject:
    requiredParameters = ['gebruikersnaam', 'gebruikersrol', 'autorisatieprotocol', 'weergave_gebruikersnaam']
    
    def __init__(self, **userParameters) -> None:
        # Initialize with default empty values or with provided parameters
        for param in self.requiredParameters:
            setattr(self, param, userParameters.get(param, None))

    def update_parameters(self, **userParameters) -> None:
        for param, value in userParameters.items():
            setattr(self, param, value)

    def validate(self) -> None:
        for param in self.requiredParameters:
            if getattr(self, param) is None:
                raise KeyError(f"Missing required parameter: {param}")

class CustomObject:
    def __init__(self, **customParameters) -> None:
        for param in customParameters:
            setattr(self, param, customParameters[param])

if __name__ == '__main__':
    event = EventObject()
    event.update_parameters(gebeurteniscode='code1')
    event.update_parameters(actiecode='action1', utcisodatetime='2023-10-10T00:00:00Z')
    # Add the rest of parameters incrementally
    event.update_parameters(identificatortype='type1', identificator='id1', aard='typeA')
    event.validate()  # Validates if all required parameters are filled

    user = UserObject(gebruikersnaam='user1')
    user.update_parameters(gebruikersrol='admin')
    # Add the rest of parameters incrementally
    user.update_parameters(autorisatieprotocol='protocol1', weergave_gebruikersnaam='User One')
    user.validate()  # Validates if all required parameters are filled

    print(vars(event))
    print(vars(user))