<?php
ini_set('display_startup_errors',1);
ini_set('display_errors',1);
error_reporting(-1);
#$a=shell_exec("python2 ../clustering/kmeans.py");
$a=exec("sh createGraph");
echo $a;
echo "hi php1";
echo shell_exec("which Rscript");
#echo shell_exec("ls -ltr /home/senguttu/public_html/drug/viz/myRscript /home/senguttu/public_html/drug/viz/loess.R");
echo "<br/>";
echo shell_exec("/usr/local/bin/Rscript /home/senguttu/public_html/drug/viz/loess.R 2>&1");
echo "<br/>";
echo "hi php2";


?>
