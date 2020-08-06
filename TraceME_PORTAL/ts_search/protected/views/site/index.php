<?php
/* @var $this SiteController */

$this->pageTitle=Yii::app()->name;
?>

<h1>Introduction</h1>
<div style="font-size: 18px;">
	<div style="float: right;width: 480px;padding: 5px; font-size: 12px; text-align:center;">
		<IMG alt="Figure 1. Time series of ice thickness anomalies in four seasons for the period 1910-2010. (Produced by CAFE)" src="<?php echo Yii::app()->request->baseUrl; ?>/images/figure2.jpg">
		<br/>
		Figure 1. Schematic diagram of the transient traceability framework. This framework traces the modeled transient carbon storage dynamics to carbon residence time, NPP, carbon storage potential, and their source factors. From Zhou et al. (2018).
	</div>
	Model inter-comarison projects (MIPs) have been used to assess differences between model outputs and explore the uncertainties among models. Such as CMIP, TRENDY. 
	<br/>
	To provide a traceability analysis tool for those MIPs and assist scientists to work efﬁciently with the development of earth system models, we propose a traceability analysis for model evluation (TraceME), a online post-MIP system. This system uses the framework of CAFE.
	<br/>
	Traceability analysis method has been applied to inter-model and inter-sites studies.
</div>
<div style="clear:both;margin:20px auto; border-bottom:1px solid #ccc;"></div>
<h1>Traceability analysis</h1>
<div style="font-size: 18px;">
	<div style="float: left;width: 520px;padding: 5px; font-size: 12px; text-align:center;">
		<IMG alt="Figure 2. Architecture of CAFE" src="<?php echo Yii::app()->request->baseUrl; ?>/images/figure1.jpg">
		<br/>
		Figure 2. Schematic diagram of the traceable components. Xss,ecosystem carbon storage capacity;τE,ecosystem carbon residence time;τE',baseline carbon residence time;ξ,environmental scalar;ξT,temperature scalar;ξW,temperature scalar.
	</div>
	CAFE is supposed to enable efficient data query and large scale collaborative analysis of environmental data. To fulfil this design goal, CAFE is designed to mainly include four parts: data index module, task managing module, data analysis module and Web-based user interface. Besides, there is a central server used for the management of global nodes and data.
	<br/><br/>
	All the nodes absorbed in CAFE network are peer to peer and united by common protocols and interfaces. CAFE consists of a server-side package and a web user interface package. The server-side package integrates index module, task managing module and data analysis module, and will be installed at each node. The web user interface package includes the web user interface and related services, can be configured at any web server.
</div>
<div style="clear:both;margin:20px auto; border-bottom:1px solid #ccc;"></div>
<h1>Workflow of TraceME</h1>
<div style="font-size: 18px;">
	<div style="float: right;width: 495px;padding: 5px; font-size: 12px; text-align:center;">
		<IMG alt="Figure 3. Sketch map of CAFE workflow." src="<?php echo Yii::app()->request->baseUrl; ?>/images/figure4.jpg">
		<br/>
		Figure 3. Sketch map of CAFE workflow.
	</div>
A typical scientific data analysis workflow in CAFE consists of the following steps:
<br/><br/>1) the user selects datasets and analytic function and submit the analysis task through the Web-based user interface; 
<br/><br/>2) the task managing module parses the task and decomposes it into several sub-tasks, where one dataset corresponds to one sub-task; 
<br/><br/>3) all the sub-tasks are dispatched to the nodes where the datasets are stored;
<br/><br/>4) all the sub-tasks are fulfilled by invoking the corresponding analytic functions locally;
<br/><br/>5) after all the sub-tasks are finished, the task managing module collects the results and sends compiled analysis results back to the user through the Web-based user interface;
<br/><br/>6) the user can download the analysis results in the last step.
</div>
<div style="clear:both;margin:20px auto; border-bottom:1px solid #ccc;"></div>
<h1>Web user interface</h1>
<div style="font-size: 18px;">
	<div style="float: right;width: 490px;padding: 5px; font-size: 12px; text-align:center;">
		<IMG alt="Figure 4. Schematic diagram of web user interface." src="<?php echo Yii::app()->request->baseUrl; ?>/images/figure5.jpg">
		<br/>
		Figure 4. Schematic diagram of web user interface.
	</div>
The web-based user interface provides a user-friendly way for researchers to query and analyze environmental data through the web browser.It mainly includes six parts, respectively are initialization, search, task submission, task list checking, task detail checking and results retrieval. If a user wants to use analytic functions in CAFE he has to register an account first, and then log in. The user can filter the dataset by specifying institute, project, frequency, etc. After selecting desired datasets to the list, the application will send a request to the node and obtain the information of available analytic functions. The user can choose the analytic function, set the corresponding parameters and submit a task.
<br/>
<br/>When the user submits the task form, the information of seleted analytic function will be queried and used to validate input parameters. The application regularly sends requests to the node to retrieve real-time status of tasks by APIs. Asynchronous refreshing is utilized to show real-time status of each task. The user can compare the results of different sub-tasks from the task detail page and download different kinds of results. The web page will demonstrate the graphs or the charts of the results and provide download links of multi-format result files.
</div>
<div style="clear:both;margin:20px auto; border-bottom:1px solid #ccc;"></div>
<h1>Software Availability&Copyright</h1>
<div style="font-size: 18px;">
	<div style="float: right;width: 440px;padding: 5px; font-size: 12px; text-align:center;">
		<IMG alt="Figure 5. EOF analysis for the period 1900-1999.(Produced by CAFE)" src="<?php echo Yii::app()->request->baseUrl; ?>/images/figure3.jpg">
		<br/>
		Figure 5. The time series of carbon storage (smooth solid lines), storage capacity (fluctuating solid lines), and carbon storage potential (shaded areas, positive above the smooth solid lines, and negative below the smooth solid lines) for those models in TRENDY. From Zhou et al. (2018).
	</div>
<br/><br/>
	TO get the full software package,please access 
        <a href="https://github.com/EcoSummerCoder/TraceME_codes">https://github.com/EcoSummerCoder/TraceME_codes</a>
        <br/>
	<br/>
	This document is written by Jian Zhou.
	<br/><br/>
	The authors of TraceME include Jianyang Xia, Jian Zhou etc.
        <br/><br/>
        If you have any questions about TraceME, please send email to us.
        <br/>
        Email: jzhou@stu.ecnu.edu.cn
        <br/><br/>
        Address:Research Center for Global Change and Ecological Forecasting, School of Ecological and Environmental Sciences, East China Normal University, Shanghai 200241, China
        <br/><br/>
        Copyright: Research Center for Global Change and Ecological Forecasting, School of Ecological and Environmental Sciences, East China Normal University
</div>
