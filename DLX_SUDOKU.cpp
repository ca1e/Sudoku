
// -----------------------------------------.cpp

CDlxSudoku::CDlxSudoku(bool bChkUnique /*= true*/)
{
    m_bChkUnique = bChkUnique;
}

int CDlxSudoku::serch(int k)
{
    if(m_head.right==&m_head)
    {
        memcpy(m_rslt, m_mem, sizeof(m_rslt));
        return 1;
    }

    node*t,*tt;
    int min=RR+1;   // 每列的元素个数不会超过 RR
    int tc;
    for(t=m_head.right;t!=&m_head;t=t->right)
    {
        if(m_cnt[t->c]<min)
        {
            min=m_cnt[t->c];
            tc=t->c;
            if(min<=1)break;
        }
    }
    remove(tc);
    int scnt = 0;
    for(t=m_col[tc].down;t!=&m_col[tc];t=t->down)
    {
        m_mem[k]=t->r;
        for(tt=t->right;tt!=t;tt=tt->right)
        {
            remove(tt->c);
        }

        scnt += serch(k+1);
        
        // 不检测唯一性且解为1 或者 检测唯一性时解大于1 
        if (!m_bChkUnique && scnt==1 || scnt>1) 
            return scnt;
        
        for(tt=t->left;tt!=t;tt=tt->left)
        {
            resume(tt->c);
        }
    }
    resume(tc);
    return scnt;
}

int CDlxSudoku::solve(string & strSudoku)
{
    int i = 0;
    int j = 0;
    while (i < strSudoku.length()) 
    {
        char num = (strSudoku.at(i)=='.') ? 0 : (strSudoku.at(i)-'0');
        if (num >=0 && num <=9)
        {
            m_ch[j++] = num;
            if (j >= 81) break;
        }
        
        ++i;
    }

    m_all_t=0;
    memset(m_cnt,0,sizeof(m_cnt));
    m_head.left=&m_head;
    m_head.right=&m_head;
    m_head.up=&m_head;
    m_head.down=&m_head;
    m_head.r=RR;
    m_head.c=CC;
    for(i=0;i<CC;i++)
    {
        m_col[i].c=i;
        m_col[i].r=RR;
        m_col[i].up=&m_col[i];
        m_col[i].down=&m_col[i];
        // 将col[i]插入在 head.left 和 head之间 (横行链表, 行的最右边)
        m_col[i].left=m_head.left;
        m_col[i].right=&m_head;
        m_col[i].left->right=&m_col[i];
        m_col[i].right->left=&m_col[i];
    }
    for(i=0;i<RR;i++)
    {
        m_row[i].r=i;
        m_row[i].c=CC;
        m_row[i].left=&m_row[i];
        m_row[i].right=&m_row[i];
        // 将row[i] 插入在 head.up 和 head 之间 (纵向链表, 列的最下边)
        m_row[i].up=m_head.up;
        m_row[i].down=&m_head;
        m_row[i].up->down=&m_row[i];
        m_row[i].down->up=&m_row[i];
    }
    for(i=0;i<RR;i++)
    {
        int r=i/9/9%9;
        int c=i/9%9;
        int val=i%9+1;
        char q = m_ch[r*9+c];
        if(q==0||q==val)
        {
            link(i,r*9+val-1);
            link(i,81+c*9+val-1);
            int tr=r/3;
            int tc=c/3;
            link(i,162+(tr*3+tc)*9+val-1);
            link(i,243+r*9+c);
        }
    }
    // 将 m_row[x] 从横向链表中删除
    for(i=0;i<RR;i++)
    {
        m_row[i].left->right=m_row[i].right;
        m_row[i].right->left=m_row[i].left;
    }
    
    int num=serch(0);
    // printf("num=%d/n",num);
    int k;
    for(i=0;i<81;i++)
    {
        j=m_rslt[i]/9%81;
        k=m_rslt[i]%9+1;
        m_ans[j]=k;
    }
    
//    for(i=0;i<81;i++)
//        printf("%d",m_ans[i]);
//    printf("/n");

//    printfSolve();
    
    return num;
}
