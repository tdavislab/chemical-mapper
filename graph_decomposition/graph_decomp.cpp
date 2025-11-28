# include <iostream>
# include <stack>
# include <unordered_map>
# include <vector>
# include <include/pybind11/pybind11.h>
# include <include/pybind11/stl.h>
using namespace std;
namespace py=pybind11;

class graph
{
    public:

    unordered_map<int,vector<int>> adj_list;
    vector<vector<int>> cycles;
    vector<vector<int>> paths;
    //int size;
    vector<vector<int>> stars;
    graph(unordered_map<int,vector<int>> input_graph)
    {
        //size = nodes;
        for(auto i:input_graph)
        {
            adj_list[i.first] = i.second; 
        }     
        

    }
    bool find_ele(stack<int> trav, int ele)
    {
      while(!trav.empty())
      {
        if(trav.top()==ele)
        {
            return true;
        }
        else{
            trav.pop();
        }
      }
      return false;
    }
    bool find_ele_vec(vector<int> back_track, int ele)
    {
      for(auto i = back_track.begin();i<back_track.end();i++)
      {
        if(*i == ele)
        {
            return true;
        }
      }
      return false;
    }
    void find_stars()
    {
        vector<int> temp;
        for(auto i: adj_list)
        {
          int count = 0;
          temp.clear();
          temp.push_back(i.first);
          if(i.second.size()>=3)
          {
            for(auto j = i.second.begin();j<i.second.end();j++)
            {
                if(adj_list[*j].size()==1)
                {
                    count++;
                    temp.push_back(*j);
                }
            }
          }

          if(count>=3)
          {
            stars.push_back(temp);
          }
        }
    }
    void find_cycles()
    {
        unordered_map<int,int> visited;
        int start = adj_list.begin()->first;
        //Initializing the visited array
        for(auto i:adj_list)
        {
            visited[i.first] = 0;
        }

        stack<int> traversed;
        stack<int> temp;
        traversed.push(start);
        visited[start]=1;
        int prev=0;
        int temp_prev;
        int flag = 0;
        while(!traversed.empty())
        {
         flag = 0;
         for(auto i = adj_list[traversed.top()].begin();i < adj_list[traversed.top()].end();i++)
         {
            if(visited[*i]==0)
            {
                prev = traversed.top();
                traversed.push(*i);
                visited[*i]=1;
                flag = 1;
                break;
            }
         }
         if(flag==0)
         {
            for(auto i = adj_list[traversed.top()].begin();i < adj_list[traversed.top()].end();i++)
            {
                if(*i != prev && find_ele(traversed,*i))
                {
                  temp=traversed;
                  vector<int> cycle;
                  cycle.push_back(*i)
;                 while(temp.top()!=*i)
                  {
                   cycle.push_back(temp.top());
                   temp.pop();
                  }
                  cycle.push_back(*i);
                  cycles.push_back(cycle);
                }
            }
            traversed.pop();
            if(!traversed.empty())
            {
                temp_prev = traversed.top();
                traversed.pop();
                if(!traversed.empty())
                {
                    prev = traversed.top();
                    traversed.push(temp_prev);
                }
                else
                {
                    prev=-1;
                    traversed.push(temp_prev);
                }
            }

         } 
        }

    }

    void del_node(int a)//Erase by key
    {
       adj_list.erase(a);
       for(auto i = adj_list.begin();i!=adj_list.end();i++)
       {
        for(auto j = i->second.begin();j<i->second.end();j++)
        {  
            if(*j == a)
            {
               i->second.erase(j);
            }
        }
       }

    }


    void branch_decomposition()// This is to be called only after removing the cycles
    {
        if(adj_list.size() != 0)
        {
            unordered_map<int,int> visited;
            //Initializing the visited array
            for(auto i:adj_list)
            {
                visited[i.first] = 0;
            }

            stack<int> traversed;
            stack<int> temp;
            int start = adj_list.begin()->first;
            traversed.push(start);
            visited[start]=1;
            int prev=0;
            int temp_prev = -1;
            int flag = 0;
            vector<int> path;
            while(!traversed.empty())
            {
            flag = 0;

            for(auto i = adj_list[traversed.top()].begin();i < adj_list[traversed.top()].end();i++)
            {
                if(visited[*i]==0 && adj_list[traversed.top()].size()>2)
                {
                    
                    if(path.size()>2)
                    {
                        paths.push_back(path);
                    }
                    path.clear();
                    traversed.push(*i);
                    visited[*i]=1;
                    flag = 1;
                    break;
                }

                else if(visited[*i]==0 && adj_list[traversed.top()].size()<=2)
                {
                        
                    traversed.push(*i);
                    visited[*i]=1;
                    flag = 1;
                    break;
                }
            }
            
            if(flag==0)
            {
            path.push_back(traversed.top());
            temp_prev = traversed.top();
            traversed.pop();
            if(traversed.empty())
            {
                if(path.size()>0)
                {
                    paths.push_back(path);
                }
                path.clear();
            }
            }
            }
            //For removing computed branches
            for(int i = 0; i<paths.size();i++)
            {
              for(int j = 0;j<paths[i].size();j++)
              {
                del_node(paths[i][j]);
              }
            }
            //Recompute the branch decomposition
            branch_decomposition();

        }

    } 
};

PYBIND11_MODULE(Graph, m) {
    py::class_<graph>(m, "graph")
        .def(py::init<unordered_map<int,vector<int>>>())
        .def("find_ele", &graph::find_ele)
        .def("find_ele_vec", &graph::find_ele_vec)
        .def("find_cycles", &graph::find_cycles)
        .def("find_stars", &graph::find_stars)
        .def("branch_decomposition",&graph::branch_decomposition)
        .def("del_node",&graph::del_node)
        .def_readwrite("adj_list",&graph::adj_list)
        .def_readwrite("cycles",&graph::cycles)
        .def_readwrite("paths",&graph::paths)
        .def_readwrite("stars",&graph::stars);
}