function waveformbig(name,filename) {
    var htmltochange = document.getElementById("graphandcaption");
    var name = document.getElementById("name").value;
    var filename = document.getElementById("filename").value;
    htmltochange.innerHTML = "<img src='/static/waveformbig/"+name+"_"+filename+".png' alt='Waveform of the whole sound file'><p>Waveform of the whole sound file</p>";
    htmltochange.innerHTML = '<div id="div8"><img src="/static/waveformbig/'+name+'_'+filename+'.png" alt="Waveform of the whole sound file" class="graph" width="auto" height="auto"></div><div><div id="div9"><p><button onclick="waveformbig();" class="button2">Large waveform</button></p><p><button onclick="waveformsmall();" class="button2">Small waveform</button></p><p><button onclick="fftbig();" class="button2">Large frequency graph</button></p><p><button onclick="fftsmall();" class="button2">Small frequency graph</button></p></div><div id="div10"><p>Waveform of the whole sound file: this graph represents the verticle shape your vase could take</p></div></div>';
}
function waveformsmall(name,filename) {
    var htmltochange = document.getElementById("graphandcaption");
    var name = document.getElementById("name").value;
    var filename = document.getElementById("filename").value;
    htmltochange.innerHTML = "<img src='/static/waveformsmall/"+name+"_"+filename+".png' alt='Waveform of one sound wave'><p>Waveform of one sound wave</p>";
    htmltochange.innerHTML = '<div id="div8"><img src="/static/waveformsmall/'+name+'_'+filename+'.png" alt="Waveform of one sound wave" class="graph" width="auto" height="auto"></div><div><div id="div9"><p><button onclick="waveformbig();" class="button2">Large waveform</button></p><p><button onclick="waveformsmall();" class="button2">Small waveform</button></p><p><button onclick="fftbig();" class="button2">Large frequency graph</button></p><p><button onclick="fftsmall();" class="button2">Small frequency graph</button></p></div><div id="div10"><p>Waveform of one sound wave: this graph represents one wave in the bottom layer of your vase</p></div></div>';
}
function fftbig(name,filename) {
    var htmltochange = document.getElementById("graphandcaption");
    var name = document.getElementById("name").value;
    var filename = document.getElementById("filename").value;
    htmltochange.innerHTML = "<img src='/static/fftbig/"+name+"_"+filename+".png' alt='Graph of the amplitudes of the frequencies 0 to 20k hz'><p>Graph of the amplitudes of the frequencies 0 to 20k hz</p>";
    htmltochange.innerHTML = '<div id="div8"><img src="/static/fftbig/'+name+'_'+filename+'.png" alt="Graph of the amplitudes of the frequencies 0 to 20k hz" class="graph" width="auto" height="auto"></div><div><div id="div9"><p><button onclick="waveformbig();" class="button2">Large waveform</button></p><p><button onclick="waveformsmall();" class="button2">Small waveform</button></p><p><button onclick="fftbig();" class="button2">Large frequency graph</button></p><p><button onclick="fftsmall();" class="button2">Small frequency graph</button></p></div><div id="div10"><p>Graph of the amplitudes of the frequencies 0 to 20k hz: Fourier transform of the sound for the human range of hearing, set your frequency to be a high point</p></div></div>';
}
function fftsmall(name,filename) {
    var htmltochange = document.getElementById("graphandcaption");
    var name = document.getElementById("name").value;
    var filename = document.getElementById("filename").value;
    htmltochange.innerHTML = "<img src='/static/fftsmall/"+name+"_"+filename+".png' alt='Graph of the amplitudes of the frequencies 0 to 500 hz'><p>Graph of the amplitudes of the frequencies 0 to 500 hz</p>";
    htmltochange.innerHTML = '<div id="div8"><img src="/static/fftsmall/'+name+'_'+filename+'.png" alt="Graph of the amplitudes of the frequencies 0 to 500 hz" class="graph" width="auto" height="auto"></div><div><div id="div9"><p><button onclick="waveformbig();" class="button2">Large waveform</button></p><p><button onclick="waveformsmall();" class="button2">Small waveform</button></p><p><button onclick="fftbig();" class="button2">Large frequency graph</button></p><p><button onclick="fftsmall();" class="button2">Small frequency graph</button></p></div><div id="div10"><p>Graph of the amplitudes of the frequencies 0 to 500 hz: Fourier transform of the sound for a useful range, set your frequency to be a high point</p></div></div>';
}