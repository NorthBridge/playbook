from milestoneDAO import MilestoneDAO

def main():
    mDao = MilestoneDAO()
    for milestone in mDao.getMilestones():
        number = milestone.create()
        if (number is None):
            print "Error when trying to create milestone."
        else:
            print "Number of new milestone [refers to \'%s\']: %d.\n" % (milestone.getTitle(), number)
        
if __name__ == '__main__':
    main()
