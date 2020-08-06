package cn.edu.tsinghua.cess.task.entity.dto;

/**
 * Created by kurt on 2014/9/22.
 */
public class SubTaskFile {

    private String type;
    private String url;
    private String filename;

    public String getUrl() {
        return url;
    }
    public void setUrl(String url) {
        this.url = url;
    }
    public String getType() {
        return type;
    }
    public void setType(String type) {
        this.type = type;
    }
    public String getFilename() {
           return filename;
    }
    public void setFilename(String filename){
         this.filename=filename;
    }
}
