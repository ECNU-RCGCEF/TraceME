package cn.edu.tsinghua.cess.task.service;

import cn.edu.tsinghua.cess.task.entity.SubTask;
//test by zhoujian:
import cn.edu.tsinghua.cess.task.entity.dto.TaskSubmition;
import java.util.*;

public interface TaskExecutionService {
	
	public void addTask(SubTask subTask );
//add by zhoujian:
	public void addTask_submited(TaskSubmition submition, List<SubTask> subTask);

}
