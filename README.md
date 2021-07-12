# Astera
An open-source, dicord bot wrote in Python and is ran in a docker container.

# Requirements
- Latest version of Python (Python 3.9.6)

- A discord application, if not make on at the discord developer pannel. Or click the link below.
- Docker
- Portainer (Optional)

# Intructions 
After you git the source, create a venv with python inside the root directoy of this project.

1. python3 -m venv (directory)
2. Edit the Astera.py file with your settings and token. (Inside the app folder)
3. Build the docker image, docker build -t xz1il/astera . (Must include the . at the end or it will fail)
4. Run the container, docker run xz1il/astera
5. Finished!

# Links
https://discord.com/developers/applications
