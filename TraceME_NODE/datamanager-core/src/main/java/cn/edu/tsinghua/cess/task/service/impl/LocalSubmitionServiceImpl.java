package cn.edu.tsinghua.cess.task.service.impl;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
//add by zhoujian
import org.apache.log4j.Logger;

import cn.edu.tsinghua.cess.modelfile.dao.ModelFileDao;
import cn.edu.tsinghua.cess.modelfile.entity.Model;
import cn.edu.tsinghua.cess.task.dao.TaskSubmitionDao;
import cn.edu.tsinghua.cess.task.entity.SubTask;
import cn.edu.tsinghua.cess.task.entity.SubTaskListEntry;
import cn.edu.tsinghua.cess.task.entity.Task;
import cn.edu.tsinghua.cess.task.entity.dto.TaskSubmition;
import cn.edu.tsinghua.cess.task.service.TaskExecutionService;
import cn.edu.tsinghua.cess.task.service.TaskSubmitionService;

@Component("localSubmitionService")
public class LocalSubmitionServiceImpl implements TaskSubmitionService {
	private Logger log = Logger.getLogger(LocalSubmitionServiceImpl.class);
    @Autowired ModelFileDao modelFileDao;
	@Autowired TaskSubmitionDao taskSubmitionDao;
	@Autowired TaskExecutionService taskExecutionService;

	@Transactional
	@Override
	public String submitTask(TaskSubmition submition) {
        String uuid = TaskIdGenerator.generateTaskId();
        Date ts = new Date();

		Task task = new Task();
        task.setUuid(uuid);
        task.setCreateTime(ts);
		task.setSubmitionEntity(submition);
        taskSubmitionDao.insert(task);
		//add by zhoujian:
		log.info("zj:local-1.subtask start!");
        List<Integer> subTaskIdList = this.submitSubTask(submition);
		//add by zhoujian:
		log.info("zj:local-2.subtask stop!");
        for (Integer id :subTaskIdList) {
					//add by zhoujian:
		log.info("zj:local-3.subtask for start!");
            SubTaskListEntry entry = new SubTaskListEntry();
            entry.setTaskId(task.getId());
            entry.setSubTaskId(id);
		//add by zhoujian:
		log.info("zj:local-4.subtask for  stop!");
            taskSubmitionDao.insertSubTaskListEntry(entry);
        }

        return uuid;
	}

    @Override
    public List<Integer> submitSubTask(TaskSubmition submition) {
        List<Integer> subTaskIdList = new ArrayList<Integer>();

        for (Model model : submition.getModels()) {
            SubTask subTask = SubTask.newInstance(model, submition.getNclScript());
		//add by zhoujian:
		log.info("zj:local-5.submition  start!");
            taskSubmitionDao.insertSubTask(subTask);
					//add by zhoujian:
		log.info("zj:local-6.submition add  start!");
            taskExecutionService.addTask(subTask);
					//add by zhoujian:
		log.info("zj:local-7.submition add stop!");
            subTaskIdList.add(subTask.getId());
					//add by zhoujian:
		log.info("zj:local-5.submition list  stop!");
        }

        return subTaskIdList;
    }

}
