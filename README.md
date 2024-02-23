# PyMTDEvaluator2
Updated version of PyMTDEvaluator with support for Multi-Criteria Decision Making Methods

## Cite us

PyMTDEvaluator was first published in [2021 IEEE 32nd International Symposium on Software Reliability Engineering (ISSRE)](https://ieeexplore.ieee.org/abstract/document/9700355). If you use the tool, please cite the following publication.

	@inproceedings{torquato2021pymtdevaluator,
  	title={Pymtdevaluator: A tool for time-based moving target defense evaluation: Tool description paper},
  	author={Torquato, Matheus and Maciel, Paulo and Vieira, Marco},
  	booktitle={2021 IEEE 32nd International Symposium on Software Reliability Engineering (ISSRE)},
  	pages={357--366},
  	year={2021},
  	organization={IEEE}
	}



### Installation

PyMTDEvaluator depends on some libraries described in the paper. 

If you are a Docker container user, please follow the recommendations below.

PyMTDEvaluator docker container requires a XWindow server. 
- Xwindow server is usually available on most Linux OSes.
- For windows and mac, the user may select the preferred XWindow server. 

**Installation Linux-specific**

#Download PyMTDEvaluator2-DockerImage.tar: Image available at: https://drive.google.com/file/d/1Qa7p5Z059ey4D0ApJX7RsHkUAAlH3TJZ/view?usp=sharing

#Loading PyMTDEvaluator image on your Docker platform

	sudo docker load < PyMTDEvaluator2-DockerImage.tar

#Checking images listing

	sudo docker images 

#Assign a tag to the downloaded image (replace <img-id> with the Image id)

	sudo docker tag <img-id> pymtdevaluator2

#Jump to your Operating System:

#Starting xhost
	
	xhost +local:root

#Running docker container:

	sudo docker run -it --rm     --env=DISPLAY     --env=QT_X11_NO_MITSHM=1     --volume=/tmp/.X11-unix:/tmp/.X11-unix:rw     pymtdevaluator2

#Inside the container

	python3 PyMTDEvaluator2.py

--NOTE

Remember that the generated files will be stored inside the container.


**For results extraction:**

	docker exec <container-ID> ./zipResults.sh
 
	docker cp <container-ID>:/Results.zip .

We recommend to start a new container for each round of evaluations. 

## Errors while using MCDM methods:

In general, errors occur when the parameters present anomalies (e.g., short time for attack success and late VM migrations, etc). Some examples are below. In case you find errors like: "raise ValueError(f"The data {values} doesn't look like a ranking")", please check your parameters. 

1) Zero value for any of the criteria

	At this version of PyMTDEvaluator, we need to have at least 1% of weight for the each of the criteria. Zero values cause errors in the data transformation for the evaluation. 

2) Errors in shorter evaluations without MTD action.

	Evaluation time shorter than the movement trigger leads to cost=0. Therefore, the MCDM method will produce errors in the evaluation. 


