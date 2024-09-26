# How to use Part_1

## Jenkins and pipeline
1. Required have an installed Jenkins with plugins: [Git](https://plugins.jenkins.io/git/), [Docker](https://plugins.jenkins.io/docker-plugin/), [Docker pipeline](https://plugins.jenkins.io/docker-workflow/), [Pipeline: Stage View](https://plugins.jenkins.io/pipeline-stage-view/) (Last one only for UI goals). And others commonly used plugins.
2. Configure Docker as a cloud: **Dashboard > Manage Jenkins > Clouds**
3. Node with Docker installed. Configure it at **Dashboard > Manage Jenkins > Nodes**.
4. I used local installed Jenkins with built-in Node, some useful commands below <details><summary>Commands</summary>
docker run -d -p 8080:8080 --name jenkins -e DOCKER_HOST=tcp://host.docker.internal:2375 jenkins/jenkins
<br /> docker exec -it -u root jenkins bash <br /> apt-get update <br /> apt-get install -y docker.io <br /> usermod -aG docker jenkins <br /> cat /var/jenkins_home/secrets/initialAdminPassword
</details>

5. Setup Pipeline. Screenshots below. <details><summary>Screenshots</summary>
**Step 1** ![Step 1](https://raw.githubusercontent.com/RomanKovalev/jnks/0c8c1eef186485995d3ff600d9a2f3ee49ff4836/part_1/readme_images/step1.png) <br /><br />
**Step 2** ![Step 2](https://raw.githubusercontent.com/RomanKovalev/jnks/0c8c1eef186485995d3ff600d9a2f3ee49ff4836/part_1/readme_images/step2.png) <br /><br />
**Step 3** ![Step 3](https://raw.githubusercontent.com/RomanKovalev/jnks/0c8c1eef186485995d3ff600d9a2f3ee49ff4836/part_1/readme_images/step3.png) <br /><br />

</details>

6. Run created pipeline. It will fall because of not setup parameter, but next times it will require parameter "URL" for success running. To avoid this it possible to setup parameter while creating pipeline.

7. Pipeline configuration storead in **part_1/Jenkinsfile**
8. An artifacts (downloaded images) could be found at successful build page.

PS. I have choosen a pipeline agent - Docker as the simplest way to achieve isolated build processing. But in real life it could be implemented in other way, depends on circumstances.

## Python script
**fetch_images.py** - It grabs all images from the webpage passed as command line argument and saves it in local folder ("images" as a default).

Asyncio and aiohttp as a processing libraries for asynchronous\simultaneous fetching tasks. 

**test_fetch_images.py** - tests for the script.

**requirements.txt** - both runtime and test dependencies.
