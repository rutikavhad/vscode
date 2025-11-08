public class simple_hashing {
    int arr[] = new int[11];

    void linear_probing(int number) {
        int hashkey = number / 10;   
        //System.out.println("Hash key: " + hashkey);
        int done = 0;

        while (done != 1) {
            if (arr[hashkey] == 0) {       
                arr[hashkey] = number;
                done = 1;
            } else {                        
                hashkey = (hashkey + 1) % arr.length;  
            }
        }
    }

    void search(int number){
        int hashkey=number%10;
        int count=0;
       while (count<arr.length) {
        if (arr[hashkey]==number) {
            System.out.println("number found "+number);
            break;
        }
        else
            hashkey=(hashkey+1)%arr.length;
            count++;
       }
       if (count==arr.length){
        System.out.println("number not found "+number);
       }
      
    }
    void delete(int number) {
        int hashkey = number / 10;
        int count = 0;

        while (count < arr.length) {
            if (arr[hashkey] == number) {
                arr[hashkey] = 0;
                System.out.println("Deleted " + number + " from index " + hashkey);
                return;
            }
            hashkey = (hashkey + 1) % arr.length;  
            count++;
        }

        System.out.println("Number " + number + " not found for delete");
    }

    void display() {
        for (int i = 0; i < arr.length; i++) {
            System.out.println("Index " + i + " → " + arr[i]);
        }
    }

    public static void main(String[] args) {
        simple_hashing hashing = new simple_hashing();

        hashing.linear_probing(11);
        hashing.linear_probing(12);
        hashing.linear_probing(13);
        hashing.linear_probing(14);
        hashing.linear_probing(15);
        hashing.linear_probing(18);
        hashing.linear_probing(17);
        hashing.linear_probing(18);
        hashing.linear_probing(20);
        hashing.linear_probing(20);
        // hashing.delete(15);
        hashing.linear_probing(23);
        // hashing.search(12);
        hashing.linear_probing(34);
        // hashing.search(44);
         hashing.display();
    }
}
