#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>

#define BUF 262144

const char *HTML =
"<!DOCTYPE html>\n"
"<html><head><meta charset='utf-8'>\n"
"<title>Assembler</title>\n"
"<style>\n"
"body{font-family:monospace;background:#111;color:#0f0}\n"
"textarea{width:100%;height:300px;background:#000;color:#0f0}\n"
"button{padding:10px;margin:10px 0}\n"
"pre{background:#000;padding:10px}\n"
"a{color:#0ff;display:block;margin-top:10px}\n"
"</style></head><body>\n"
"<h2>Assembler (Single Page)</h2>\n"

"<p>This will:\n"
   "\t- supports db/dw/dd/dq/resb/resd/resq/rest\n"
   "\t- supports mov reg, imm ; mov reg, reg ; mov reg, [symbol] ; mov reg, [reg+reg*scale+disp]\n"
   "\t- supports add/sub/xor/cmp/push/pop/inc/dec/mul/div/jmp/int\n"

   "FILE FORMAT MUST BE:\n"
    "\tsection .data\n"
    "\tsection .bss\n"
    "\tsection .text\n"
    "\t;comments allow\n"
"</p>\n"

"<textarea id='asm'></textarea><br>\n"
"<button onclick='run()'>Assemble</button>\n"
"<a href='/download'>Download output.bin</a>\n"
"<pre id='out'></pre>\n"
"<script>\n"
"function run(){\n"
"fetch('/',{method:'POST',headers:{'Content-Type':'text/plain'},body:document.getElementById('asm').value})\n"
".then(r=>r.text()).then(t=>document.getElementById('out').textContent=t)\n"
".catch(e=>alert(e));}\n"
"</script></body></html>";

int main() {
    int s = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(8080);

    bind(s, (struct sockaddr*)&addr, sizeof(addr));
    listen(s, 10);

    printf("Open http://localhost:8080\n");

    while (1) {
        int c = accept(s, NULL, NULL);

        char req[BUF];
        int n = read(c, req, sizeof(req)-1);
        if (n <= 0) { close(c); continue; }
        req[n] = 0;

        /* -------- DOWNLOAD BIN -------- */
        if (strstr(req, "GET /download") != NULL) {
            FILE *f = fopen("output.bin", "rb");
            if (!f) {
                dprintf(c, "HTTP/1.1 404 Not Found\r\n\r\n");
                close(c);
                continue;
            }
            dprintf(c,
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/octet-stream\r\n"
                "Content-Disposition: attachment; filename=\"output.bin\"\r\n\r\n");

            char b[1024];
            size_t r;
            while ((r = fread(b,1,sizeof(b),f))>0)
                write(c,b,r);
            fclose(f);
        }

        /* -------- POST = ASSEMBLE -------- */
        else if (strstr(req, "POST / ") != NULL) {

            /* find content length */
            int content_len = 0;
            char *cl = strstr(req, "Content-Length:");
            if (cl) content_len = atoi(cl + 15);

            char *body = strstr(req, "\r\n\r\n");
            if (!body) { close(c); continue; }
            body += 4;

            int header_bytes = body - req;
            int already = n - header_bytes;

            FILE *f = fopen("input.asm", "wb");
            fwrite(body, 1, already, f);

            int remaining = content_len - already;
            while (remaining > 0) {
                int r = read(c, req, sizeof(req));
                if (r <= 0) break;
                fwrite(req, 1, r, f);
                remaining -= r;
            }
            fclose(f);

            system("./assembler input.asm output.bin");

            FILE *out = fopen("terminal_output.txt","r");
            char text[BUF] = {0};
            if (out) {
                fread(text,1,sizeof(text)-1,out);
                fclose(out);
            }

            dprintf(c,
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "Connection: close\r\n\r\n"
                "%s", text);
        }

        /* -------- GET / (MAIN PAGE) -------- */
        else {
            dprintf(c,
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n\r\n%s", HTML);
        }

        close(c);
    }
}
