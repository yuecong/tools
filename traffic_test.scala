import sys.process._
import java.io.IOException

val MAX_THREAD = args(0).toInt;
var totalTime:Long = 0;
val now = System.nanoTime;
//println(MAX_THREAD);
def readURL()= {
  val url1 = "https://www.yahoo.com/";
  //val url1 ="http://10.4.17.63:8081/chart1.html";
  try{
   io.Source.fromURL(url1)
  } catch{
      case e: Exception => { e.printStackTrace(); e.toString() }
  } finally {
  val processTime = (System.nanoTime - now) /1000/1000; //million seconds
  totalTime = List(totalTime,processTime).max;
  println(" Total Process Time: %d ms".format(totalTime));
  }
}
// get URL cocurrently 
for (i <- 1 to  MAX_THREAD ) {
    val thread = new Thread {
        override def run {
            readURL();
        }
    }
    thread.start
    //Thread.sleep(50) // slow the loop down a bit
}

//println("HERE!!!!!");

 

