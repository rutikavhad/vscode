#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Register encoding (3 bits each)
struct Reg 
{
    char *name;
    char *bin;
};

struct Reg registers[] = 
{
    {"eax", "000"},
    {"ecx", "001"},
    {"edx", "010"},
    {"ebx", "011"},
    {"esp", "100"},
    {"ebp", "101"},
    {"esi", "110"},
    {"edi", "111"}
};

#define NUM_REGS 8

// Function to get register binary code
const char* get_reg_code(const char *reg)
{
    for (int i = 0; i < NUM_REGS; i++) 
    {
        if (strcmp(reg, registers[i].name) == 0) 
	{
            return registers[i].bin;
        }
    }
    return NULL;
}

// Convert binary string to integer
int bin_to_int(const char *bin) 
{
    int val = 0;
    while (*bin) 
    {
        val = (val << 1) | (*bin - '0');
        bin++;
    }
    return val;
}

int main() 
{
    FILE *fp = fopen("mod_rm.asm", "r");
    if (!fp) 
    {
        perror("Error opening 24111066.asm");
        return 1;
    }

    FILE *out = fopen("sib_output.txt", "w");
    if (!out) {
        perror("Error opening modrm_output.txt");
        fclose(fp);
        return 1;
    }

    char line[256];
    while (fgets(line, sizeof(line), fp)) 
    {
        char *token = strtok(line, " ,\t\n");

        if (token && strcmp(token, "mov") == 0) 
	{
            char *dest = strtok(NULL, " ,\t\n");
            char *src  = strtok(NULL, " ,\t\n");

            const char *dest_code = get_reg_code(dest);
            const char *src_code  = get_reg_code(src);

            if (dest_code && src_code) 
	    {
                // Mod = 11 (register-direct mode)
                char modrm_bin[9];
                snprintf(modrm_bin, sizeof(modrm_bin), "11%s%s", src_code, dest_code);

                int modrm_val = bin_to_int(modrm_bin);

                printf("%s %s %s -> ModR/M: 0x%x\n", token, dest, src, modrm_val);
                fprintf(out, "%s %s %s -> ModR/M: 0x%x\n", token, dest, src, modrm_val);
            }
        }
    }

    fclose(fp);
    fclose(out);

    return 0;
}

