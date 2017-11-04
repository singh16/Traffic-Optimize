#include<queue>
#include<iostream>
#include <sstream>
#include <vector>
#include <string.h>
using namespace std;


int *parent= nullptr; //This Parent array whch is used to store all the parent vertex of all the vetercies

struct Edge // Structure is used to store both Source and destination of the Edge in structure object format further in code
{
    int src, dest;
};

/* recover path for the given destination recursively */
void recoverPath(int parent[], int des)
{  // Printing the output in given format vertex1-vertex2-vertex3
    if (parent[des] == des)
    {
        cout << des;
    }
    else
    {
        recoverPath(parent, parent[des]);
        cout << "-" << des;
    }
}


// class to represent a graph object
class Graph
{
    int N;

public:
    // A array of vectors to represent adjacency list
    vector<int> *adjList;
    Graph(int N)    // Constructor

    {
        this->N = N; //Intializeing the total number of vertices
        adjList = new vector<int>[N]; // Creating the vector list of size N
    }

    void EdgeFill(vector<Edge> edges)
    {
        // add edges to the undirected graph
        for (auto i:edges)
        {
            int src = i.src;
            int dest = i.dest;
            // As it is undirected graph so we add one edge from source to des and des to source
            adjList[src].push_back(dest);
            adjList[dest].push_back(src);
        }
    }
};

// Perform BFS on graph starting from vertex v
int BFS(Graph const &graph, int v, vector<bool> &discovered, int des)
{
    parent[v] = v;
    // create a queue used to do BFS
    queue<int> q;

    // mark source vertex as discovered
    discovered[v] = true;

    // push source vertex into the queue
    q.push(v);

    // run till queue is not empty
    while (!q.empty())
    {
        // pop front node from queue and print it
        v = q.front();
        q.pop();
        if (v == des)
        {
            break;
        }
        //cout << v << " ";

        // do for every edge (v -> u)
        for (int u : graph.adjList[v])
            if (!discovered[u] && parent[u] == -1)
            {
                // mark it discovered and push it into queue
                discovered[u] = true;
                parent[u] = v;
                q.push(u);
            }
    }
    return 0;
}


int main()
{
    int TotalV=-1;  // Total number of Vertices Initializing it with 0 (Invalid)
    vector <Edge> e; // This is to maintain Edge set
    int ctr = 0; // This is to increase the size of vector size on the basis of edges entered
    string line1; // This is to take command from the user
    int flagE=0;
    while (!cin.eof())
    {

        line1=""; // command is cleared to take new user command again
        getline(cin,line1); // Taking user input
	//cout<<line1;
        if(cin.eof())  // checking for eof condition
        {
            break;     // Break the the while loop if end of file condition is met
        }

        stringstream forCmdCheck(line1);// converting user string command to stream
        char firstchar='X'; // initializing character with invalid character X everytime
        forCmdCheck>>firstchar; // Taking command character from stream
        stringstream cmdstream(line1);


        if ( firstchar== 'V'|| firstchar== 'v')
        {
            char removec; // removing V character
            cmdstream>>removec>>TotalV;// fetching number of vertices in TotalV variable
            if (TotalV < 0) // checking for Invalid number of vertices
            {
                cerr<<"Error: number of vertices must be positive."<<"\n";
            }
            else
            {

                if ( e.size()!=0 ||flagE==1) // free the old graph
                {
                    e=vector<Edge>(); // free the edges vector array by making its size 0
                    flagE=0;
                    delete(parent); // free the parent array
                }

                parent= new int[TotalV]; // Dynamically allocating memory to the parent array to retrace back shortest Path
		//cout<<"V "<<TotalV<<endl;
            }
        }

        else if (firstchar== 'E' || firstchar== 'e')
        {
            if (TotalV < 0) // Checking if E command is follwed by Valid V command
            {
                cerr << "Error: First Enter the Number of Vertices\n";
                continue;
            }
            if(line1.length() ==4)
            {  flagE=1;
                continue;
            }

            if(e.size()>0 ||flagE==1) // Checking if there is already a valid edge vector array
            {
                cerr << "Error: Edges Already Entered\n";
                continue;
            }

            e=vector<Edge>(); // To reset the edge every time new edges come

            int from=0, to=0; // from and to variable is to trace every edge
            char cremove; // Remove E character
            cmdstream>>cremove>>cremove;

            while (!cmdstream.eof())
            {
                cmdstream>>cremove>>from>>cremove>>to>>cremove; // Tracing every input edge that is its from vertex and to vertex
                if (from < 0 || from >= TotalV || to < 0 || to >= TotalV) //make sure the vertices are valid (0 to V - 1)
                {
                    cerr << "Error: the pair is invalid.\n";// If the vertices are out of range we clears the edges vector array anf break
                    e=vector<Edge>();
                    break;
                }
                else
                { /* otherwise, add into the Edges(e) vector array */
                    ctr = ctr + 1;
                    e.reserve(ctr); // increasing size of the vector array
                    e.push_back({ from,to }); // adding both from vertex and to vertex in e
                }

                /* get next pair */
                cmdstream>>cremove;
                if(cremove!=',') //As after the the last vertex pair (Edge) there is no comma so we will come out of while edge reading loop
                {flagE=1; break;}
            }

        }

        else if (firstchar== 's'|| firstchar== 'S')
        {
            if (TotalV < 0 || flagE==0) // Checking if s command is followed by valid V and Valid E command
            {

                cerr << "Error: Please Enter both Vertices and Edges before getting shortest path\n";
                continue;
            }

            int source=0, destination=0; // variable source and destination in which shortest distance is to be found
            char cremove; // variable to remove s command
            cmdstream>>cremove>>source>>destination;
            if (source < 0 || source >= TotalV || destination < 0 || destination >= TotalV) /*make sure the from vertex and source vertex are valid (0 to V - 1) */
            {
                cerr << "Error: Source and Destination both should be in valid Range\n";
                continue;
            }

            // create a graph from edges
            Graph graph(TotalV); //Creating Graph object and passing the Total vertices in constructor object
            graph.EdgeFill(e);  // Filling the edges in vector data structure

            for (int i=0;i<TotalV;i++) // initializing the Parent array with -1 as initially we dont know parent of any vertex
            {
                parent[i]=-1;
            }

            vector<bool> discovered(TotalV);// stores vertex is discovered or not


            BFS(graph, source, discovered, destination);   // Do BFS traversal from all undiscovered nodes to
                                                           // cover all unconnected components of graph
            if (parent[destination] == -1) // Checking if we discovered parent vertex of the destination
            {
                /* no path found, display an error */
                cerr<< "Error: No path exist\n";
            }
            else
            {
                recoverPath(parent, destination); // Recovering the shortest path by backtracking the Parent array
                cout<<"\n";
            }

        }


    }

    if (e.size()!=0)   /* free all the dynamic memory allocated before exiting the Program */
    {
        e=vector<Edge>();//free the Edges set by making it's size 0
        flagE=0;
        delete(parent);// Free the parent Array
    }
    return 0;
}