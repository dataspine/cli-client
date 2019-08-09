# Dataspine CLI reference

![Dataspine Logo](http://s3.amazonaws.com/dataspine/dataspine-logo-black.png)


### Dataspine CLI commands
```
spinectl help

### EXPECTED OUTPUT ###
...

get deployments             <-- Displays a list of deployments on the cluster
get services                <-- Displays a list of service endpoints on the cluster

help                        <-- This List of CLI Commands

login			 			<-- Authenticates the user with Dataspine backend

model build 				<-- Packages the model code into a container image 
model build-manifest 	    <-- Generates a build manifest (Dockerfile) for the model/project
model build-logs 			<-- Displays logs for the model build job
model deploy 				<-- Deploys model on cluster
model endpoint 				<-- Displays the endpoint uri for a deployed model
model init 					<-- Creates a model/project directory structure 
 

predict create-route 		<-- Creates traffic routes for the deployed model endpoint  
predict test				<-- Pings the model server with a test request file 
predict delete-route		<-- Deletes traffic routes for the deployed model endpoint 

version                     <-- View This CLI Version
```


# Dataspine CLI concepts

Use the Dataspine CLI to create, manage, and deploy your own models to your Kubernetes cluster seamlessly and in a predictive way.

Configure dataspine to use your existing kubernetes cluster in a tenant-managed and secure way. 

Using the Dataspine cli is easy, you just need to get used to some concepts you are probably already familiar with

### Login
First of all, make sure you are provided with credentials to use the CLI, once you have them, login simply by running `dataspine login` and you'll be prompted for your username and password


### Managing your clusters
Cluster: The model entity of a kubernetes cluster. Use this subcommand to manage your clusters into the Dataspine platform. Tag them, name them, and upload your configuration securely
To manage the cluster use the subcommand `dataspine cluster <action>`

#### Actions
`create`: Creates a cluster entity in your account. Make sure you name it a proper name, an alias if you want, and a description to keep your clusters organized

`init`: Links your cluster to the dataspine platform 

`list`: List all of your clusters

### Managing your models

You know better your AI and ML projects, whatever it is the framework you are using, you can build and deploy it with dataspine. 
Use the CLI to build your model into a container ready to run on any kubernetes cluster. Use `dataspine model <action>`

`build`: Let dataspine know where your model is and run this command to build your model. Dataspine will take care from here and get your docker image ready.
`push`: Once your image is ready, push the model to make it available to the dataspine platform. 
`deploy`: Use this command to create a kubernetes deployment running your model
`pull`: Download your models from anywhere pulling them from the dataspine platform. 

## Quick Start

To start using dataspine you can use your own models or you can test building a test model from the repo `git@github.com:dataspine/dataspine-notebook-environment.git`

Navigate to `notebooks/keras/ccfd` for a keras example. We'll build it. 

The command to do it is `dataspine model build` and you need to provide the following information

`--model-name`: The name of your model. Can be whatever works for you
`--model-tag`: The tag of the docker image to be built. Tip: You can add your version here
`--model-type`: The type of the model, in this case, it'd be Keras
`--model-path`: Point to where your model is. If you moved to the directory pointed above, you should enter `.

Once you set that up, run the command and wait for it to finish. It can take some time, but after it's done, you'll have a docker image built with the name and tag that you provided.

Once built, we need to push the model. You'll use `dataspine model push` providing the specific `--model-name` and `--model-tag`. This will push the model to the dataspine repository and make it available for deploy.

You are now ready to deploy your model, make sure you have a Kubernetes cluster and that you or your cluster administrator has added the cluster and its proper configs to the Dataspine platform

Now you simply deploy your model using `dataspine model deploy` and make sure you provide the following arguments

`--model-name`: The name of your model. 
`--model-tag`: The tag of the docker image.
`--cluster-name`: The name that your cluster has in the Dataspine platform
`--namespace`: This is optional, if you need to deploy your model in a specific namespace that already exists, then use it.

That's it! you already have a running model in you kubernetes cluster in 3 simple commands.
