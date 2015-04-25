import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future
import scala.concurrent.duration._

object trafficTest {


 def main(args:Array[String]) {
   val test_count_concurrent =  if (args.length > 0) args(0).toInt else 5
 
   def readURL(url:String) = {
    //Access indicated URL, and return the process time in million seconds.
    //If there is some error/exception,e.g. no response error, return -1 as error. 
    //Get the Content with io.Source package
    val start = System.nanoTime;io.Source.fromURL(url);val process_time = (System.nanoTime - start) /1000/1000 //million seconds
    process_time
   } 

    val urls_sample = Seq("http://openvswitch.org/","http://www.alliedtelesis.com","http://www.alliedtelesis.com");
    val urls = List.fill(test_count_concurrent)(urls_sample).flatten.take(test_count_concurrent) // get the test urls
    println(urls)
    val seq_read_urls = urls.map(url => Future(readURL(url)))
    //val seq_read_urls = List (Future(readURL("https://www.yahoo.com/")) ,Future(readURL("http://www.alliedtelesis.com")))
    val read_url_tests = Future sequence seq_read_urls
    val process_times = concurrent.Await.result(read_url_tests, 10.minutes)

    println("Test Count:" + process_times.length)
    println("Min:" + process_times.min +"ms")
    println("Avg:" + process_times.sum / process_times.length +"ms")
    println("Max:" + process_times.max +"ms")
    println("Total:" + process_times.sum +"ms")


}
 
}
