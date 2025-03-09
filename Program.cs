using System;
using tpmodul4_103022300071;

namespace tpmodul4_103022300071
{
    class Program
    {
        public static void Main(string[] args)
        {
            KodePos kodePos = new KodePos();

            kodePos.DisplayAllKodePos();
            Console.WriteLine();
            Console.WriteLine("\nSimulasi DoorMachine:");
            DoorMachine door = new DoorMachine();

            door.BukaPintu(); 
            door.BukaPintu(); 
            door.KunciPintu(); 
            door.KunciPintu(); 
        }
    }
}
