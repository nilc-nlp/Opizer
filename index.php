<?php 
require('texts/projects/Opizer/sumarios/index.php');
require('includes/projects/Opizer/sumarios/tmp.php');  
?>

<div class="masthead">
    <a style="text-decoration:None;" href="index.php"><h1 class="text-muted"><?php echo $title; ?></h1></a>

    <div class="bs-example bs-example-tabs">
    <ul id="myTab" class="nav nav-tabs" style="margin-bottom:5px;">
            <li rel="tooltip" title="<?php echo $tooltip_menu_ferramenta;?>" class="active"><a href="#ferramenta" data-toggle="tab"><?php echo $ferramenta; ?></a></li>
           <!-- <li rel="tooltip" title="<?php echo $tooltip_menu_sobre;?>" class=""><a href="#sobre" data-toggle="tab"><?php echo $sobre; ?></a></li> -->
        </ul>
        <div id="myTabContent" class="tab-content">
            <div class="tab-pane fade" id="sobre">
		<br/>
                <?php echo $introducao1; ?>
                <?php echo $introducao2; ?>


		<div class="page-header">
			<h3><?php echo $referencias;?></h3>
		</div>
            </div>
            <div class="tab-pane fade active in" id="ferramenta">
                    <div class="well">
                        <div class="list-group-item">
<span class="label label-default"><?php echo $input_sentence;?></span>
<div class="list-group-item">
<?php echo $select_item;?>:
<select id="items">
  <option value="0">Samsung Galaxy S-III</option>
  <option value="1">Samsung Smart TV</option>
  <option value="2">LG Smart TV</option>
  <option value="3">Iphone 5</option>
  <option value="4"> Capitães da Areia</option>
  <option value="5"> Crepúsculo</option>
  <option value="6"> Ensaio sobre a Cegueira</option>
  <option value="7"> Fala sério, Amiga!</option>
  <option value="8"> Fala sério, Amor!</option>
  <option value="9"> Fala sério, Mãe!</option>
  <option value="10"> Fala sério, Pai!</option>
  <option value="11"> Fala sério, Professor!</option>
  <option value="12"> O Apanhador nos Campos de Centeio</option>
  <option value="13"> O Outro lado da meia noite</option>
  <option value="14"> O Reverso da Medalha</option>
  <option value="15"> Se houver Amanhã</option>
  <option value="16"> 1984</option>
</select>
<br><br> 
<table>
  <col width="160">
  <col width="160">
  <tr>
    <td><?php echo $extractive_method;?></td>
    <td><?php echo $abstractive_method;?></td>
  </tr>
  <tr>
    <td><input type="radio" name="summarizer" value="opizere" checked>Opizer-E</td>            
    <td><input type="radio" name="summarizer" value="opizera">Opizer-A</td>    
  </tr>

  <tr>
  <td><input type="radio" name="summarizer" value="huliu">Hu Liu</td>
  <td><input type="radio" name="summarizer" value="ganesan">Ganesan</td>
  </tr>
    <tr>
    <td><input type="radio" name="summarizer" value="tadano">Tadano</td>
    <td><input type="radio" name="summarizer" value="gerani">Gerani</td>              
  </tr>
</table>
<br>
<?php echo $num_aspects;?>: <input id="aspects" size=2 maxlength=2 onKeyPress="return numbersonly(this, event)">
</div>
                  <div class="row">
                                <div class="text-center">

                                    <br/>
                                    <div id="submit-simple">
                                        <button id="button_normalizar" class="btn btn-default" onclick="Opizer.call_python('button_normalizar');"><?php echo $normalize;?></button>
                                    </div>

                                </div>
                            </div>

                            <span class="label label-success"><?php echo $normalized_sentence;?></span>
                            <div contenteditable="false" id="output_sentence" class="form-control uneditable-input" rows=3 disabled style="background-color: white; color:black; height:auto; overflow:visible; min-height:70px;"></div>

                            <div class="text-center">
                                <br/>
                                <button type="button" class="btn btn-default btn-mini" onclick="Opizer.clean();"><?php echo $clean;?></button>
                            </div>
                        </div>
                    </div>

            </div>

        </div>
    </div>




<script type="text/javascript">
<!--
// copyright 1999 Idocs, Inc. http://www.idocs.com
// Distribute this script freely but keep this notice in place
function numbersonly(myfield, e, dec)
{
var key;
var keychar;

if (window.event)
   key = window.event.keyCode;
else if (e)
   key = e.which;
else
   return true;
keychar = String.fromCharCode(key);

// control keys
if ((key==null) || (key==0) || (key==8) ||
    (key==9) || (key==13) || (key==27) )
   return true;

// numbers
else if ((("0123456789").indexOf(keychar) > -1))
   return true;

// decimal point jump
else if (dec && (keychar == "."))
   {
   myfield.form.elements[dec].focus();
   return false;
   }
else
   return false;
}

//-->
</script>
<script src="dist/js/projects/Opizer/my_app.js"></script>
