<h1>BIOART WITH ECHO BOTS AND PYTHON</h1>

<h2>Using the Bioprinter Python Package</h2>


<p>The <strong>BIOPRINTER</strong> is a Python package for producing living art with Echo robots. It transforms an image into files that a ECHO 
  liquid dispenser can use to print the image to a plate using pigmented yeast or bacteria.</p>
  
<p>You can find out more about this package at the:<a href="https://github.com/Edinburgh-Genome-Foundry/bioprinter">EDIMBURGH GENOME FOUDRY</a>.</p>
  
<code>pip install ez_setup bioprinter</code>.</p>



<h2>What you should know</h2>


<p>The files displayed in this repository are part of a 4-step process to print Bioart. Here´s how it goes:</p>


<p><ol>
  <li>Find a image<ul>
      <li>The image needs to have blue as Background color</li>
      <li>The image needs to be in <strong>jpeg format</strong> </li>
  </ul></li>
  <li>Convert the image into a CSV file <ul>
      <li>Open a copy of the standard code of Byoprinter on your local Python text editor</li>
      <li>adjust the colors to match the ones at your image to their wells.</li>
      <li>Run the code.</li>
      <li>Get the CSV file on the file folder containing your Pythin code.</li>
  </ul></li>
  <li>Edit the CSV file<ul>
      <li>Make sure the number of wells you are using per color on the <strong>plate</strong> match the ones in the <strong>CSV file </strong> </li>
      <li>Pour liquid colored liquid cultures in ECHO well plates</li>
  </ul></li>
   <li>Print your art<ul>
      <li>Get a Agar plate with culture media</li>
      <li>Get your ECHO plate with the colors</li>
      <li>Get the adjusted CSV file</li>
      <li>Feed them all to your ECHO liquid dispenser and start the protocol.</li>
      
  </ul></li>
</ol>
  </p>
