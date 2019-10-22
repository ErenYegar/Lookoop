#include <vector>
#include <iostream>

#include "util.hpp"

using namespace std;

/**
 * ����������������ͷ���
 * @param list �����б�
 * @return Node*
 */
ListNode* get_link_list(const vector<int>& list) {
	ListNode *head = new ListNode;
	ListNode *dummy = head;
	for (auto it = list.begin(); it != list.end(); ++it) {
		ListNode *tmp = new ListNode(*it);
		dummy->next = tmp;
		dummy = tmp;
	}
	return head->next;
}
