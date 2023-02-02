import json

import main

def test_simple():
    """Test that with no preferences and ample tables, each legislator will be assigned to their own table"""
    simple_test_soln = main.solve(5, ["A", "B", "C", "D", "E"], [])
    print(f"Simple solution: {json.dumps(simple_test_soln)}") 
    assert len(simple_test_soln) == 5, "Failed simple test"

def test_limited_tables():
    """Test that with limited tables, all legislators will be grouped together with no preferences"""
    limited_tables_soln = main.solve(3, ["A", "B", "C", "D", "E"], [])
    print(f"Limited tables solution: {json.dumps(limited_tables_soln)}") 
    assert len(limited_tables_soln) == 1, "Failed limited tables test"

def test_avoid_no_merge():
    """Test that legislators will not sit together in max solution"""
    avoid_nomerge_soln = main.solve(3, ["A", "B", "C", "D", "E"], [{"preference": "avoid", "guests": ["A", "B"]}])
    print(f"Avoid (no merge) solution: {json.dumps(avoid_nomerge_soln)}") 
    assert len(avoid_nomerge_soln) == 2

def test_avoid_withmerge():
    """Test that when the tables have to be merged, avoid preferences will be respected"""
    avoid_merge_soln = main.solve(2, ["A", "B", "C", "D", "E"], [{"preference": "avoid", "guests": ["A", "B"]}])
    print(f"Avoid (with merge) solution: {json.dumps(avoid_merge_soln)}")
    assert len(avoid_merge_soln) == 2

def test_no_soln():
    """"Test that we return no solution if solution is impossible"""
    no_soln = main.solve(1, ["A", "B", "C", "D", "E"], [{"preference": "avoid", "guests": ["A", "B"]}])
    print(f"Result for no solution: {json.dumps(no_soln)}")
    assert no_soln == []

def test_example_soln():
    """Test with example shown during interview"""
    example_soln = main.solve(3, ["A", "B", "C", "D", "E"], [
        {"preference": "pair", "guests": ["A", "B"]}, 
        {"preference": "pair", "guests": ["D", "B"]},
        {"preference": "pair", "guests": ["E", "C"]},
        {"preference": "avoid", "guests": ["C", "D"]}])
    print(f"Result for example solution: {json.dumps(example_soln)}")
    assert len(example_soln) == 2

test_simple()
test_limited_tables()
test_avoid_no_merge()
test_avoid_withmerge()
test_no_soln()
test_example_soln()
