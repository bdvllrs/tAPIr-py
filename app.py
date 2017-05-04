from API_config import API_CONFIG
from models.Programs import Programs

if __name__ == '__main__':
    CONFIG = API_CONFIG('http://localhost/api')

    programs = Programs(CONFIG)
    print(programs.put(_id=1, mane='test'))
