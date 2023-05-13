import googletasks
import notion


#tasks that already exist
#check why due date not going 



def main():    
    misc, coursework = notion.notion()
    print(misc)
    print(coursework)
    googletasks.googletasks(misc, coursework)

if __name__ == "__main__":
    main()




