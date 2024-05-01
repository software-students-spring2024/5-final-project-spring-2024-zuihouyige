# Final Project
[![Flask CI/CD](https://github.com/software-students-spring2024/5-final-project-spring-2024-zuihouyige/actions/workflows/CICD.yml/badge.svg)](https://github.com/software-students-spring2024/5-final-project-spring-2024-zuihouyige/actions/workflows/CICD.yml)
[![log github events](https://github.com/software-students-spring2024/5-final-project-spring-2024-zuihouyige/actions/workflows/event-logger.yml/badge.svg)](https://github.com/software-students-spring2024/5-final-project-spring-2024-zuihouyige/actions/workflows/event-logger.yml)


An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.


## How to run
[Deploy](http:/)
You can also use [Docker Desktop](https://www.docker.com/products/docker-desktop/).
Create a local repository using the following command:
    
    git clone https://github.com/software-students-spring2024/5-final-project-spring-2024-zuihouyige.git

After navigating to the local repository, run the following command (you must ensure that Docker Desktop is running).

    docker-compose down

To install the required dependencies and run the program, run the following command. Once the required dependencies have been installed the first time, the command can be run without the --build tag.

    docker-compose up --build

To use the app, open a web browser and navigate to [localhost:5002](http).
## Team Members

-[Yinyi Wen](https://github.com/YY35n)

-[Jinqiao Cheng](https://github.com/jinqiaocheng163)

-[Zhengyang Han](https://github.com/Hmic1102)