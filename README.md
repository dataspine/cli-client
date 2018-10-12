# Dataspine CLI

Use the dataspine CLI to create, manage, and deploy your own models to your kubernetes cluster seamlessly and in a predictive way.

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