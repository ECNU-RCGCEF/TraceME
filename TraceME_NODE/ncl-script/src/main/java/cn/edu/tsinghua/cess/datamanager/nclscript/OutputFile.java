/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package cn.edu.tsinghua.cess.datamanager.nclscript;

import java.io.File;

/**
 *
 * @author ericxuhao
 */
public class OutputFile {
    String outputType;
    String[] outputAlias;
    File[] outputFile;
    String[] outputArgName;
    int count;
    OutputFile(){}
    OutputFile(String outputType,String[] outputAlias,String[] outputArgName,int count){
        this.outputType=outputType;   
        this.outputAlias=outputAlias;  
        this.count=count; 
        this.outputArgName=outputArgName;  
        this.outputFile=new File[this.count];
    }
}
