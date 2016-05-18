<?php
// Turn off all error reporting
error_reporting(0);

$latLong = $_GET['latLong'];
$ar = (explode (",",$latLong));
$lat = $ar[0];
$long = $ar[1];
//echo 'result = '.$lat.', '.$long.' ';

$im = imagecreatefrompng('http://maps.googleapis.com/maps/api/staticmap?center='.$lat.','.$long.'&zoom=21&format=png&sensor=false&size=1x1&maptype=roadmap&style=feature:administrative|visibility:off&style=feature:landscape|color:0x000000&style=feature:water|color:0xffffff&style=feature:road|visibility:off&style=feature:transit|visibility:off&style=feature:poi|visibility:off&key=AIzaSyDxHFdrjoh7jkYtd8F3YYEY5XcKj_W2Vj8');
//get pixel color, put it in an array
$color_index = imagecolorat($im, 0, 0);//Get the index of the color of a pixel
$color_tran = imagecolorsforindex($im, $color_index);//Get the colors for an index

//if, for example, red value of the pixel is 1 we are on land
/*echo $color_index;
echo $color_tran['green'];
echo $color_tran['red'];
echo $color_tran['blue'];*/
if($color_tran['red'] == 255 && $color_tran['blue'] == 255 && $color_tran['green'] == 255  ){
    //do your thing
    echo "0";//NOT on land
}else{
    echo "1"; //on land
}

?>