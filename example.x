
typedef string message<32>;

program exampleProgram
{
    version exampleVersion
    {
        void hello     ( void )  = 1;
    } = 1;
    version exampleVersion2
    {
        int hello     ( message )  = 1;
    } = 2;
} = 0x20001002;
