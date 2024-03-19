# Interface for observer
class Observer():
    def update(self, value):
        pass

# Implementing obersevr
class UserObserver(Observer):
    def __init__(self, user) -> None:
        self.user =user

    def update(self, value):
        print(f'User {self.user_id} counter updated to {value}')

