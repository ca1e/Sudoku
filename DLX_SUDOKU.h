--------------------------------------- .h
#ifndef _DLX_SUDOKU_H_
#define _DLX_SUDOKU_H_
#include <string>

using namespace std;


#define RR      729             // 81 * 9
#define CC      324             // 81 * 4

struct node
{
    int r,c;
    node *up;
    node *down;
    node *left;
    node *right;
};

// dlx 算法求数独的解
class CDlxSudoku
{
public:
    CDlxSudoku(bool bChkUnique = true);
    int solve(string & strSudoku);
    void printfSolve();
    
private:
    inline void link(int r,int c)
    {
        m_cnt[c]++;
        node *t=&m_all[m_all_t++];
        t->r=r;
        t->c=c;
        t->left=m_row[r].left;
        t->right=&m_row[r];
        t->left->right=t->right->left=t;
        
        t->up=m_col[c].up;
        t->down=&m_col[c];
        t->up->down=t->down->up=t;
    }
    
    inline void remove(int c)
    {
        node *t,*tt;
        m_col[c].right->left=m_col[c].left;
        m_col[c].left->right=m_col[c].right;
        for(t=m_col[c].down;t!=&m_col[c];t=t->down)
        {
            for(tt=t->right;tt!=t;tt=tt->right)
            {
                m_cnt[tt->c]--;
                tt->up->down=tt->down;
                tt->down->up=tt->up;
            }
        }
    }
    
    inline void resume(int c)
    {
        node *t,*tt;
        for(t=m_col[c].down;t!=&m_col[c];t=t->down)
        {
            for(tt=t->left;tt!=t;tt=tt->left)
            {
                m_cnt[tt->c]++;
                tt->down->up=tt;
                tt->up->down=tt;
            }
        }    
        m_col[c].left->right=&m_col[c];
        m_col[c].right->left=&m_col[c];
    }

    int serch(int k);
   

    bool m_bChkUnique;  // 做解是否唯一的校验
    char m_ch[81];      // 输入字符，已经转换为(0-9)
    node m_head;
    node m_all[RR*4];
    node m_row[RR];
    node m_col[CC];
    int  m_cnt[CC];
    int  m_mem[81];     // 保存选择的行号
    int  m_rslt[81];    // 保存解中选择的行号
    int  m_ans[81];     // 答案 9*9
    int  m_all_t;       // m_all[] 中使用元素的下标
};


#endif  // _DLX_SUDOKU_H_
