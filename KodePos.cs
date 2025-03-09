using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace tpmodul4_103022300071
{
    public class KodePos
    {
        private Dictionary<string, string> kodePosTable;

        public KodePos()
        {
            kodePosTable = new Dictionary<string, string>
        {
            { "Batununggal", "40266" },
            { "Kujangsari", "40287" },
            { "Mengger", "40267" },
            { "Wates", "40256" },
            { "Cijaura", "40287" },
            { "Jatisari", "40286" },
            { "Margasari", "40286" },
            { "Sekejati", "40286" },
            { "Kebonwaru", "40272" },
            { "Maleer", "40274" },
            { "Samoja", "40273" }
        };
        }

        public string GetKodePos(string kelurahan)
        {
            if (kodePosTable.ContainsKey(kelurahan))
            {
                return kodePosTable[kelurahan];
            }
            else
            {
                return "Kelurahan tidak ditemukan.";
            }
        }

        public void DisplayAllKodePos()
        {
            Console.WriteLine("Daftar Kode Pos:");
            foreach (var entry in kodePosTable)
            {
                Console.WriteLine($"{entry.Key}: {entry.Value}");
            }
        }
    }
}
