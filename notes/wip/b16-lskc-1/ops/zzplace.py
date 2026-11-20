import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts2'))
import dsl
OK = ['ok:fields-place']
dsl.PLACEUP = {
 'cal.1960-04.vietnam-hanoi': {'tags_add': OK},
 'cal.1960-07-15.vietnam-hanoi': {'place': 'hanoi'},
 'cal.1960-10-20.vietnam-hanoi': {'place': 'kontum'},
 'cal.1961-02.vietnam-hanoi-2': {'tags_add': OK},
 'cal.1961-02-15.vietnam-hanoi': {'place': 'war-zone-d'},
 'cal.1961-07-27.vietnam-hanoi': {'tags_add': OK},
 'cal.1961-07.vietnam-hanoi-4': {'tags_add': OK},
 'cal.1962-09-06.vietnam-hanoi': {'tags_add': OK},
 'cal.1962-10-11.vietnam-hanoi-2': {'place': ['haiphong', 'ca-mau']},
 'cal.1963-05-14.vietnam-hanoi-2': {'tags_add': OK},
 'cal.1964-10-11.vietnam-hanoi': {'tags_add': OK},
 'cal.1965-04-27.vietnam-hanoi': {'tags_add': OK},
 'cal.1965-07-22.vietnam-hanoi': {'place': 'dong-xoai'},
}
