package cn.edu.tsinghua.cess.task.service.impl;

import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import javax.annotation.PostConstruct;

import org.apache.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import cn.edu.tsinghua.cess.task.dao.TaskSubmitionDao;
import cn.edu.tsinghua.cess.task.entity.SubTask;
import cn.edu.tsinghua.cess.task.service.TaskExecutionService;
import cn.edu.tsinghua.cess.task.service.impl.executor.TaskExecutor;
import cn.edu.tsinghua.cess.task.service.impl.executor.TaskExecutorFactory;
//test by zhoujian:
import cn.edu.tsinghua.cess.task.entity.dto.TaskSubmition;
import cn.edu.tsinghua.cess.task.service.impl.executor.TaskSubmitionExecutor;
//import cn.edu.tsinghua.cess.task.service.TaskSubmitionService;

@Component
public class TaskExecutionServiceImpl implements TaskExecutionService {
	
	private Logger log = Logger.getLogger(getClass());
	
	@Autowired TaskExecutorFactory factory;
    @Autowired TaskSubmitionDao taskSubmitionDao;
	private ExecutorService service;

	@Override
	public void addTask(SubTask subTask) {
		log.info("adding task to scheduler, taskId=" + subTask.getId() + ", taskSubmition=" + subTask);
		
		TaskExecutor executor = factory.getTaskExecutor(subTask);
		log.info("zhoujian:executor:["+executor+"]");
		service.submit(executor);
	}
//test by zhoujian:for the submition file handled togeter.	
	@Override
	public void addTask_submited(TaskSubmition submition,List<SubTask> subtask) {
		log.info("zhoujian:test addTask_submitted class!!");
		log.info("zhoujian: test the addTask_submitted class["+submition.getNclScript()+"]");
		
		TaskSubmitionExecutor executor = factory.getTaskExecutor_submition(submition,subtask);
		log.info("zhoujian:executor:["+executor+"]");
		service.submit(executor);
	}

	@SuppressWarnings("unused")
	@PostConstruct
	private void init() {
		service = Executors.newFixedThreadPool(3);
		
		log.info("execution service initializing, will load running task into scheduler");

        List<SubTask> runningSubTaskList = taskSubmitionDao.listRunningSubTask();
        if (runningSubTaskList != null) {
            for (SubTask t : runningSubTaskList) {
            	try {
            		this.addTask(t);
            	} catch (Exception e) {
            		log.error("error adding task on initialization", e);
				} 
            }
        }
	}

}
