using System;
using Rainbow.MergeEngine;
using System.IO;

namespace ConsoleApplication1
{
	/// <summary>
	/// Summary description for Class1.
	/// </summary>
	class Class1
	{
		/// <summary>
		/// The main entry point for the application.
		/// </summary>
		[STAThread]
		static void Main(string[] args)
		{
            string line;

            Console.WriteLine("Loading old.html ...");
            StreamReader srOld = new StreamReader(@"old.html");
            string strOld = string.Empty;
            while ((line = srOld.ReadLine()) != null)
            {
                strOld += line;
            }
            srOld.Close();
            Console.WriteLine("Length of old.html: {0} characters", strOld.Length);
            Console.WriteLine("");

            Console.WriteLine("Loading new.html ...");
            StreamReader srNew = new StreamReader(@"new.html");
            string strNew = string.Empty;
            while ((line = srNew.ReadLine()) != null)
            {
                strNew += line;
            }
            srNew.Close();            

            Console.WriteLine("Length of new.html: {0} characters", strNew.Length);

            Console.WriteLine("");

            Console.WriteLine("Parsing the files ...");
            DateTime dtParse = DateTime.Now;
            Merger merger = new Merger(strOld, strNew);
            strOld = string.Empty;
            strNew = string.Empty;
            TimeSpan tsParse = DateTime.Now - dtParse;

            Console.WriteLine("Number of Words in Original File: {0} ", merger.WordsInOriginalFile);
            Console.WriteLine("Number of Words in Modified File: {0} ", merger.WordsInModifiedFile);
            Console.WriteLine("Parsing Time: {0} ms", tsParse.TotalMilliseconds);

            Console.WriteLine("");

            Console.WriteLine("Merging the files ...");
            DateTime dtMerge = DateTime.Now;
            string result = merger.merge();
            TimeSpan tsMerge = DateTime.Now - dtMerge;
            TimeSpan tsTotal = DateTime.Now - dtParse;
            Console.WriteLine("Comparing & Merging Time: {0} ms", tsMerge.TotalMilliseconds);
            
            Console.WriteLine("");

            Console.WriteLine("-----------------------------------------");
            Console.WriteLine("Total Time: {0} ms", tsTotal.TotalMilliseconds);

            Console.WriteLine("");

            Console.WriteLine("Saving merged file to merged.html ...");
            StreamWriter sw = new StreamWriter("merged.html");
            sw.Write(result);
            sw.Close();

            Console.WriteLine("Using browser to view the merged file");
            Console.WriteLine("Press any key to finish ..");
            
            Console.ReadLine();
        }
	}
}
