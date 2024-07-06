---
slug: /introduction/installation
sidebar_position: 10
---

# Installation & Setup

Therix is available to install via [pypi.org](https://pypi.org/) for use in any python project. 
If you need a custom solution get in touch at [enterprise@therix.ai](mailto:enterprise@therix.ai)


## Installation
To install Therix, you'll need to use a tool called `pip`, which helps manage software packages in Python. Open your command prompt or terminal, and type the following command exactly as shown:
`pip install therix` 


## Setup 

After installing add `TTHERIX_API_KEY` in your .env file 


### Steps to create a Therix Api Key

        1. Sign up on [Therix Cloud](https://cloud.dev.therix.ai)


        2. Create a project and create an API KEY from the Api key section


After setting up Api Key in your env, you can begin using `therix` by importing it into your Python scripts. Here’s how you can start with the `Agent` class:

```python
from therix.core.agent import Agent

# Initialize a new agent
agent = Agent(name="My New Published Agent")
(agent
    .add(// Add configurations you want to add)
    .save())

    agent.publish()
    answer = agent.invoke(text)
```


#### Note

You can continue using `therix-sdk` without creating an account on therix cloud by simply adding these environment variables 

```python
THERIX_DB_HOST="your_db_host"
THERIX_DB_PORT="your_db_port"
THERIX_DB_USERNAME="your_db_username"
THERIX_DB_PASSWORD="your_db_password"
THERIX_DB_NAME="your_db_name"
THERIX_DB_TYPE="postgresql"     // Currently we only support PostgreSQL 
```


Use the `Agent` object to manage and execute various tasks within your project. For further details, follow the documentation precisely.

### Python Versions Supported

- **3.12**


<!-- ### Optional ENV VARS

Cache, etc -->