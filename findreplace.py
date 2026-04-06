import re
with open('/Users/saika_w/.openclaw/workspace/personal-task-dashboard/task-dashboard.html', 'r') as f:
    data = f.read()

old_pos = '''            if (event && item) {
                const rect = item.querySelector('.archive-task-name').getBoundingClientRect();
                const modalWidth = 600;
                const modalHeight = 400;
                const padding = 12;
                
                // Calculate position: right of task, center vertically with task name!
                let left = rect.right + padding + 20;
                let top = rect.top + (rect.height / 2) - (modalHeight / 2);
                
                // Prevent going off right edge
                if (left + modalWidth > window.innerWidth - padding) {
                    left = rect.left - modalWidth - padding - 20;
                }
                
                // Prevent going off bottom edge
                if (top + modalHeight > window.innerHeight - padding) {
                    top = window.innerHeight - modalHeight - padding;
                }
                
                // Prevent going off top edge
                if (top < padding) {
                    top = padding;
                }
                
                modalContent.style.left = left + 'px';
                modalContent.style.top = top + 'px';
                modalContent.style.transform = '';
            } else {'''

new_pos = '''            if (event && item) {
                const rect = item.querySelector('.archive-task-name').getBoundingClientRect();
                const modalWidth = 600;
                const modalHeight = 200;
                
                let left = rect.right + 10; // 10px right of task
                let top = rect.top;
                
                modalContent.style.left = left + 'px';
                modalContent.style.top = top + 'px';
                modalContent.style.transform = '';
            } else {'''

data = data.replace(old_pos, new_pos)

with open('/Users/saika_w/.openclaw/workspace/personal-task-dashboard/task-dashboard.html', 'w') as f:
    f.write(data)

print('Positioning modified')
