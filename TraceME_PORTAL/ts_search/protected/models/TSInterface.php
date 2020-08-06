<?php
define('TSInterfaceROOT','http://localhost:3011/node_TraceME_dev_w');
//define('TSInterfaceROOT_G3','http://58.198.178.51:3011/node_w1');
class TSInterface {
	
	public static function get($name){
		$data = array(
			'G1' => '/api/v1/modelfile/query/filter',
			'G2' => '/api/v1/task/submit',
			'G3' => '/api/v1/task/query',
			'G6' => '/api/v1/modelfile/query',
		);
		if(isset($data[$name])){
  //                     if ($name=='G3')
  //                        {
  //                         return TSInterfaceROOT_G3. $data[$name];
  //                         }
  //                       else
  //                        {
			return TSInterfaceROOT. $data[$name];
    //                      }
		}
		else{
			return '';
		}
	}
}

?>
