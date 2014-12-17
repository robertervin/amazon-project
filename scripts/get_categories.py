from categories.models import Category
import amazonproduct
import lxml


api = amazonproduct.API(cfg=config)

root_categories = [
        ('Clothing, Shoes, Jewelry and Watches', 7141123011),
        ('Android Apps', 2350149011),
        ('Books', 283155),
        ('Kindle Store', 133140011),
        ('Magazine Subscriptions', 599858),
        ('Movies & TV', 2625373011),
        ('CD and Vinyl', 5174),
        ('Digital Music', 163856011),
        ('Video Games', 468642), 
        ('Electronics', 172282),
        ('Cell Phones & Accessories', 2335752011),
        ('Appliances', 2619525011),
        ('Software', 229534),
        ('Musical Instruments', 11091801),
        ('Office and School Supplies', 1064954),
        ('Home & Kitchen', 1055398),
        ('Patio, Lawn & Garden', 2972638011),
        ('Tools & Home Improvement', 228013),
        ('Arts and Sewing', 2617941011),
        ('Pet Supplies', 2619533011),
        ('Grocery & Gourmet Food', 16310101),
        ('Health, Household & Baby Care', 3760901),
        ('Beauty', 3760911),
        ('Toys & Games', 165793011),
        ('Baby', 165796011),
        ('Sports & Outdoors', 3375251),
        ('Automotive Parts & Accessories', 15684181),
        ('Business, Industrial & Scientific Supplies', 16310091)
    ]

count = 0

def set_children(parent, result):
    try:
        try:
            children = result.BrowseNodes.BrowseNode.Children.BrowseNode
        except: #Base Case
            return
        else:
            for child in children:
                global count
                count = count + 1
                if count % 50 == 0:
                    print "Created " + str(count) + " Children..."
                if Category.objects.filter(node_id=child.BrowseNodeId).count() > 0:
                    continue
                child_obj = parent.add_child(name=child.Name.text, node_id=child.BrowseNodeId)
                result = api.browse_node_lookup(child_obj.node_id)
                set_children(child_obj, result)
    except:
        print("Node Lookup Failed In: " + str(children))
        pass
    
def init():
    """
    Adds all root nodes first, then recursively iterates through the children and assigns the nodes accordingly.     
    """
    root = Category.add_root(name="Amazon Categories", node_id=0)
    for root_category, root_id in root_categories:
        print root_category
        parent = root.add_child(name=root_category, node_id=root_id)
        result = api.browse_node_lookup(root_id)
        set_children(parent, result)

init()