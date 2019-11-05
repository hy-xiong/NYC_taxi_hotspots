function drawLegend(colors, colorOpacity, values, title, canvasCtrl){
	var totalHeight = canvasCtrl.height;
	var totalWidth = canvasCtrl.width;
	var ctx = canvasCtrl.getContext("2d");
	ctx.clearRect(0, 0, totalWidth, totalHeight);
	var nClass = colors.length;
	var rowSpace = Math.floor(totalHeight / (nClass + 1));
	var rowGapSpace = Math.floor(rowSpace * 0.2);
	var squareLength = Math.floor(rowSpace * 0.5);
	var titleSize = _setLabelSize(ctx, [title], rowSpace - rowGapSpace, totalWidth, true);
	var initialLabelSize = (rowSpace - rowGapSpace) * 0.5;
	_drawText(ctx, title, 0, titleSize, titleSize, true)
	labels = [];
	for (var i = 0; i < colors.length; i++){
		text = _padZero(values[i], 3) + " - " + _padZero(values[i+1], 3);
		labels.push(text);
	}
	var labelFontSize = _setLabelSize(ctx, labels, initialLabelSize, totalWidth - squareLength - 10, false);
	for(var i = 0; i < colors.length; i++){
		if(i == 0)
			_drawSquare(ctx, 0, rowSpace * (i+1), squareLength, colors[i], 0.2);
		else
			_drawSquare(ctx, 0, rowSpace * (i+1), squareLength, colors[i], colorOpacity);
		_drawText(ctx, labels[i], squareLength + 10, rowSpace * (i+1) + labelFontSize, labelFontSize, false);
	}
}

function _drawSquare(canvasContext, startX, startY, length, color, fillOpacity){
	canvasContext.globalAlpha = fillOpacity;
	canvasContext.fillStyle = color;
	canvasContext.fillRect(startX, startY, length, length);
	canvasContext.globalAlpha = 1.0;
	canvasContext.lineWidth = 1.5;
	canvasContext.strokeStyle = "#000000";
	canvasContext.strokeRect(startX, startY, length, length);
}

function _setLabelSize(canvasContext, texts, fontSize, maxWidth, bold){
	fontPrefix = "";
	if(bold == true)
		fontPrefix = "bold ";
	canvasContext.font = fontPrefix + fontSize.toString() + "px Arial";
	for (var i = 0; i < texts.length; i++){
		while(canvasContext.measureText(texts[i]).width > maxWidth){
			fontSize--;
			canvasContext.font = fontPrefix + fontSize.toString() + "px Arial";
		}
	}
	return fontSize;
}

function _drawText(canvasContext, text, startX, startY, fontSize, bold){
	canvasContext.globalAlpha = 1.0;
	canvasContext.fillStyle = "#000000";
	fontPrefix = "";
	if(bold == true)
		fontPrefix = "bold ";
	canvasContext.font = fontPrefix + fontSize.toString() + "px Arial";
	canvasContext.fillText(text, startX, startY);
}

function _padZero(value, precision){
	var roundV = Math.round(value * Math.pow(10, precision)) / Math.pow(10, precision);
	var str = roundV.toString();
	var valueSplit = str.split('.');
	if(valueSplit.length > 1){
		var floatingLength = valueSplit[1].length;
		if(floatingLength < precision){
			str += "0" * (precision - floatingLength);
		}
	}else{
		str += "." + "0" * precision;
	}
	return str
}