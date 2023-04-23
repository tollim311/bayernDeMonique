<!DOCTYPE html>
<html>

<?php

session_start();
$_SESSION['files']=[];
$_SESSION['stats']=['Pass through penalty area', 'Pass who lead to a shot'];

if($dossier = opendir('./StatsBomb/Data')){
   while(($fichier = readdir($dossier))){
        if($fichier!="." && $fichier!=".." && $fichier==""){
            array_push($_SESSION['files'],$fichier);
        }
   }
}

?>

    <head>
        <meta charset="utf-8">
        <title>Bayern de Monique</title>
        <link rel="stylesheet" href="css/style_test.css"/>
    </head>
    <body>
        <form action="POST">
            <label>Files</label>
                <select name="files">
                    <?php

                        foreach($_SESSION['files'] as $f){
                            echo"<option value=$f>$f</option>";
                        }
                    
                    ?>
                </select>
            <label>Statistique to show</label>
                <select name="files">
                    <?php

                        foreach($_SESSION['stats'] as $s){
                            echo"<option value=$s>$s</option>";
                        }
                    
                    ?>
                </select>

        </form>
    </body>

<?php

//exec("./test.sh");

?>